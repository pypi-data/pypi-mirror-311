from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    ListView,
    ListItem,
    Label,
    Static,
    Log,
    Select,
    SelectionList,
)
from textual.containers import Container, Horizontal, VerticalScroll, Grid
from rich.text import Text
from textual.binding import Binding
import asyncio
from enum import Enum
from datetime import datetime
import esptool
import sys
from io import StringIO
import json
import qube_nic.eeprom as eeprom
from textual.reactive import reactive
import serial.tools.list_ports
from textual.screen import ModalScreen, Screen
from textual import on
from textual import work
from pathlib import Path


class FlashStatus(Enum):
    IDLE = ("IDLE", "grey50")
    FAILED = ("FAILED", "red")
    SUCCESS = ("SUCCESS", "green")
    FLASHING = ("FLASHING", "yellow")


class StatusLabel(Static):
    """A widget to display the current status."""

    def __init__(self):
        super().__init__()
        self.status = FlashStatus.IDLE

    def set_status(self, status: FlashStatus):
        self.status = status
        self.update(f"[{status.value[1]} bold]{status.value[0]}[/]")


class DeviceInfo(Static):
    """A widget to display device information."""

    # Add reactive values
    hardware_id = reactive[int](0)
    serial_port = reactive[str]("")  # Add reactive serial port

    def __init__(self, device_config: dict):
        super().__init__()
        self.device_name = device_config["name"]
        self.device_config = device_config
        self.status_label = StatusLabel()
        self.is_flashing = False
        # Initialize the reactive values
        self.hardware_id = device_config["hardware_id"]
        self.serial_port = device_config["serial_port"]

    def compose(self) -> ComposeResult:
        yield Label(f"Selected Device: {self.device_name}", id="device-title")
        yield Horizontal(
            Container(
                Container(
                    VerticalScroll(
                        Label("Configuration", id="config-title"),
                        Label("Hardware ID:", classes="key"),
                        Label(
                            str(self.hardware_id),
                            id="hardware-id-value",
                            classes="value",
                        ),
                        Label("Device Manufacturer Code:", classes="key"),
                        Label(
                            str(self.device_config["device_manufacturer_code"]),
                            classes="value",
                        ),
                        Label("Firmware File Path:", classes="key"),
                        Label(
                            self.device_config["firmware_file_path"], classes="value"
                        ),
                        Label("WiFi SSID:", classes="key"),
                        Label(self.device_config["wifi_ssid"], classes="value"),
                        Label("WiFi Password:", classes="key"),
                        Label(self.device_config["wifi_password"], classes="value"),
                        Label("Serial Port:", classes="key"),
                        Label(
                            str(self.serial_port),
                            id="serial-port-value",
                            classes="value",
                        ),  # Add id for serial port
                    ),
                    id="device-details",
                ),
                self.status_label,
                id="left-panel",
            ),
            Container(Label("Flash Log:"), Log(highlight=True), id="right-panel"),
            id="main-panels",
        )

    def watch_serial_port(self, value: str) -> None:
        """React to changes in serial port."""
        if self.is_mounted:
            # Update the label directly
            serial_port_label = self.query_one("#serial-port-value")
            serial_port_label.update(str(value))
            # Update the device config as well
            self.device_config["serial_port"] = value

    async def on_mount(self) -> None:
        """Called when widget is mounted."""
        # Initialize both reactive values
        self.query_one("#hardware-id-value").update(str(self.hardware_id))
        self.query_one("#serial-port-value").update(str(self.serial_port))

    class LogStream(StringIO):
        """Custom stream to capture and redirect output to the log widget."""

        def __init__(self, log_widget, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.log_widget = log_widget

        def write(self, text):
            if text.strip():  # Only write non-empty lines
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_widget.write(f"[{timestamp}] {text}\n")
            return super().write(text)

        def flush(self):
            pass

    def generate_eeprom_file(self) -> None:
        """Generate the EEPROM file for the device."""
        obj = eeprom.EEPROMBuilder(size=512)

        wifi_ssid = self.device_config["wifi_ssid"].encode()
        wifi_pass = self.device_config["wifi_password"].encode()
        hardware_id = self.device_config["hardware_id"]
        device_manu_code = self.device_config["device_manufacturer_code"]

        # Add values to EEPROM
        obj.add(key="WIFI_SSID", value=wifi_ssid, format_char="33s", start_address=2)
        obj.add(key="WIFI_PASS", value=wifi_pass, format_char="64s", start_address=40)
        obj.add(
            key="HARDWARE_ID", value=hardware_id, format_char="<I", start_address=106
        )
        obj.add(
            key="DEVICE_MANUFACTURER_CODE",
            value=device_manu_code,
            format_char="<I",
            start_address=112,
        )
        obj.add(key="TRAP_IN_BOOT_MODE", value=0, format_char="B", start_address=120)
        obj.add(key="OTA_DEVICE_ID", value=0, format_char="<I", start_address=122)

        # Generate the files
        obj.generate_binary_file("tmp.bin")

    def update_hardware_id(self):
        log_widget = self.query_one(Log)

        # Increment hardware_id and update config.json
        try:
            # Read current config
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)

            # Find and update the current device's hardware_id
            for device in config:
                if device["name"] == self.device_name:
                    device["hardware_id"] += 1
                    # Update the reactive hardware_id
                    self.hardware_id = device["hardware_id"]
                    # Update the device_config
                    self.device_config["hardware_id"] = device["hardware_id"]
                    break

            # Write updated config back to file
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)

            timestamp = datetime.now().strftime("%H:%M:%S")
            log_widget.write(f"[{timestamp}] Hardware ID incremented successfully!\n")

        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_widget.write(
                f"[{timestamp}] [red]Failed to update hardware ID: {str(e)}[/red]\n"
            )

    async def flash_device(self, increment_hardware_id: bool = True) -> None:
        """Flash ESP8266 device using esptool API."""
        if self.is_flashing:
            return

        self.generate_eeprom_file()

        self.is_flashing = True
        log_widget = self.query_one(Log)
        self.status_label.set_status(FlashStatus.FLASHING)

        try:
            # Clear previous logs
            log_widget.clear()
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_widget.write(f"[{timestamp}] Starting flash process...\n")

            # Create custom stream for capturing output
            log_stream = self.LogStream(log_widget)

            # Store original stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            try:
                # Redirect stdout and stderr to our custom stream
                sys.stdout = log_stream
                sys.stderr = log_stream

                nic_fw_bin_path = Path(__file__).parent / "wifi-nic-r3-v2.5.2.bin"

                # Run esptool in a separate thread
                await asyncio.to_thread(
                    esptool.main,
                    [
                        "--before",
                        "default_reset",
                        "--after",
                        "hard_reset",
                        "--chip",
                        "esp8266",
                        "--port",
                        self.serial_port,
                        "--baud",
                        "921600",
                        "write_flash",
                        "0x0",
                        str(nic_fw_bin_path),
                        "0x3fb000",
                        "tmp.bin",
                    ],
                )

                # Update status to success
                self.status_label.set_status(FlashStatus.SUCCESS)
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_widget.write(f"[{timestamp}] Flash completed successfully!\n")

                if increment_hardware_id:
                    self.update_hardware_id()

            except esptool.FatalError as e:
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_widget.write(f"[{timestamp}] Flash failed: {str(e)}\n")
                self.status_label.set_status(FlashStatus.FAILED)

            finally:
                # Restore original stdout and stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                log_stream.close()

        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_widget.write(f"[{timestamp}] Error: {str(e)}\n")
            self.status_label.set_status(FlashStatus.FAILED)

        finally:
            self.is_flashing = False

    def _update_progress(self, progress: float, log_widget: Log) -> None:
        """Update the flash progress in the log."""
        if progress % 10 == 0:  # Update every 10%
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_widget.write(f"[{timestamp}] Writing at {progress:.1f}%\n")


class ComPortSelector(ModalScreen):
    """A modal for selecting COM ports."""

    def __init__(self, ports: list[tuple[str, str]]):
        super().__init__()
        self.ports = ports

    def compose(self) -> ComposeResult:
        port_items = [(f"{port[0]} - {port[1]}", port[0]) for port in self.ports]
        yield Grid(
            Label("Select COM Port", id="modal-title"),
            SelectionList[str](*port_items, id="port-list"),
            id="port-dialog",
        )

    @on(SelectionList.SelectedChanged)
    def handle_selection(self, event: SelectionList.SelectedChanged) -> None:
        """Handle COM port selection."""
        selected = event.selection_list.selected
        if selected:
            # Get the selected port
            selected_port = selected[0]
            # Dismiss the modal with the selected port
            self.dismiss(selected_port)


class DeviceScreen(Screen):
    """A screen to display device information."""

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("q", "quit", "Quit"),
        Binding("escape", "show_menu", "Back to Menu"),
        Binding("n", "program_next", "Program Next Device"),
        Binding("r", "retry_current", "Retry"),
        Binding("c", "change_port", "Change COM Port"),
    ]

    def __init__(self, device_config: dict):
        super().__init__()
        self.device_info = DeviceInfo(device_config)
        # Port will be selected via modal after screen is shown

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)
        yield self.device_info
        yield Footer()

    async def on_mount(self) -> None:
        """Show port selector when screen is mounted."""
        # Show COM port selector immediately when screen is mounted
        available_ports = self.app.get_available_ports()
        if not available_ports:
            self.app.notify("No COM ports found!", severity="error")
            return

    @work
    async def action_change_port(self) -> None:
        """Handle changing the COM port."""
        # port = await self.show_port_selector()

        available_ports = self.app.get_available_ports()
        if not available_ports:
            self.app.notify("No COM ports found!", severity="error")
            return None

        port = await self.app.push_screen(
            ComPortSelector(available_ports), wait_for_dismiss=True
        )

        if port is not None:
            # Update the reactive serial port in device_info
            self.device_info.serial_port = port
            self.app.notify(f"COM Port changed to {port}")

    async def action_program_next(self) -> None:
        """Handle programming next device."""
        await self.device_info.flash_device()

    def action_retry_current(self) -> None:
        """Handle retrying current device."""
        asyncio.create_task(self.device_info.flash_device(increment_hardware_id=False))


class QubeNICFlasher(App):
    """A Textual app to flash Qube NICs."""

    CSS_PATH = "menu.tcss"
    TITLE = "Qube NIC Flasher"

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("q", "quit", "Quit"),
        Binding("escape", "show_menu", "Back to Menu", show=False),
        Binding("n", "program_next", "Program Next Device"),
        Binding("r", "retry_current", "Retry"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)

        # Load device configurations from config.json
        try:
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, "r") as f:
                self.devices = json.load(f)
        except Exception as e:
            self.log.error(f"Error loading config.json: {e}")
            self.devices = []

        # Create main container with dynamic list items
        yield Container(
            Label(f"Where will the NIC be attached", id="title"),
            ListView(
                *(
                    ListItem(
                        Label(
                            Text.from_markup(
                                f"{i+1}. {device['name']}\n[dim]{device['description']}[/dim]"
                            )
                        )
                    )
                    for i, device in enumerate(self.devices)
                ),
                id="menu",
            ),
            id="main-container",
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_show_menu(self) -> None:
        """Show the main menu screen."""
        self.pop_screen()

    async def action_program_next(self) -> None:
        """Handle programming next device."""
        if isinstance(self.screen, DeviceScreen):
            await self.screen.device_info.flash_device()

    def action_retry_current(self) -> None:
        """Handle retrying current device."""
        if isinstance(self.screen, DeviceScreen):
            asyncio.create_task(
                self.screen.device_info.flash_device(increment_hardware_id=False)
            )

    def get_available_ports(self) -> list[tuple[str, str]]:
        """Get list of available COM ports."""
        return [
            (port.device, port.description)
            for port in serial.tools.list_ports.comports()
        ]

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle the selection of a menu item."""
        # Get the selected device config
        selected_device = self.devices[event.list_view.index]
        # Push the device screen without specifying port
        await self.push_screen(DeviceScreen(selected_device))


def main():
    app = QubeNICFlasher()
    app.run()

if __name__ == "__main__":
    main()
