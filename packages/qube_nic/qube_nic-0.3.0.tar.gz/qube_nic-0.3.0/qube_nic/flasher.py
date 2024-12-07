import sys
import json
import os
import qube_nic.eeprom as eeprom
import subprocess

try:
    import tty
    import termios
except ModuleNotFoundError:
    pass
from datetime import datetime
from rich.console import Console

console = Console()

KEEP_GOING = True
TEMP_EEPROM_FILE_NAME = "nic-eeprom.bin"
CONFIGURATION_FILE = "configuration.json"


# define our clear function
def clear_screen():

    # for windows
    if os.name == "nt":
        _ = os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system("clear")


class KeyPress:
    def __init__(self):
        self.is_windows = os.name == "nt"
        if self.is_windows:
            import msvcrt

    def getch(self):
        """Gets a single character from standard input without requiring Enter.
        Works on both Windows and Unix-like systems."""
        if self.is_windows:
            import msvcrt

            return msvcrt.getch().decode("utf-8")
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def get_config() -> dict:
    with open(CONFIGURATION_FILE, "r") as f:
        config = json.load(f)

    return config


def save_config(config: dict):
    with open(CONFIGURATION_FILE, "w") as f:
        json.dump(config, f, indent=2)


def generate_eeprom():
    config = get_config()
    console.print(config)

    """This function is automatically called after firmware has been uploaded."""
    obj = eeprom.EEPROMBuilder(size=512)

    wifi_ssid = config["wifi_ssid"].encode()
    wifi_pass = config["wifi_password"].encode()
    hardware_id = config["hardware_id"]
    device_manu_code = config["device_manufacturer_code"]

    # Add values to EEPROM
    obj.add(key="WIFI_SSID", value=wifi_ssid, format_char="33s", start_address=2)
    obj.add(key="WIFI_PASS", value=wifi_pass, format_char="64s", start_address=40)
    obj.add(key="HARDWARE_ID", value=hardware_id, format_char="<I", start_address=106)
    obj.add(
        key="DEVICE_MANUFACTURER_CODE",
        value=device_manu_code,
        format_char="<I",
        start_address=112,
    )
    obj.add(key="TRAP_IN_BOOT_MODE", value=0, format_char="B", start_address=120)
    obj.add(key="OTA_DEVICE_ID", value=0, format_char="<I", start_address=122)

    # Generate the files
    obj.generate_binary_file(TEMP_EEPROM_FILE_NAME)


def monitor_process(command):
    """
    Monitors and displays real-time output from a process.

    Args:
        command (list): Command to execute as a list of strings
    """
    try:
        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            universal_newlines=True,  # Return string output instead of bytes
            bufsize=1,  # Line buffered
        )

        print(f"\n[{datetime.now()}] Started process: {' '.join(command)}")
        print("-" * 60)

        # Continuously read and display output
        while True:
            output = process.stdout.readline()

            # Break if process has finished and no more output
            if output == "" and process.poll() is not None:
                break

            if output:
                # Strip any trailing whitespace and print with timestamp
                output = output.rstrip()
                print(f"{output}")

                # Ensure output is displayed immediately
                sys.stdout.flush()

        # Get the return code
        return_code = process.poll()
        print("-" * 60)
        print(f"[{datetime.now()}] Process finished with return code: {return_code}")

        return return_code

    except KeyboardInterrupt:
        print("\nProcess monitoring interrupted by user")
        process.terminate()
        return 1
    except Exception as e:
        print(f"\nError monitoring process: {e}")
        return 1


def flash():
    config = get_config()
    serial_port = config["serial_port"]
    firmware_path = config["firmware_file_path"]

    # python esptool.py -p /dev/tty.usbserial-0001 -b 460800 --before default_reset --after hard_reset --chip esp8266 write_flash --flash_mode dio
    #  --flash_size detect --flash_freq 40m 0x0 build/bootloader/bootloader.bin 0x8000 build/partition_table/partition-table.bin 0x10000 build/hello_world.bin

    exit_code = monitor_process(
        [
            "poetry",
            "run",
            "esptool.py",
            "--before",
            "default_reset",
            "--after",
            "hard_reset",
            "--chip",
            "esp8266",
            "--port",
            serial_port,
            "--baud",
            "115200",
            "write_flash",
            "0x0",
            firmware_path,
            "0x3fb000",
            TEMP_EEPROM_FILE_NAME,
        ]
    )

    if exit_code == 0:
        console.print("PASS", style="bold green")
    else:
        console.print(f"FAIL ({exit_code})", style="bold red")


def post_flashing():
    global KEEP_GOING
    config = get_config()

    # get next command
    key_reader = KeyPress()
    print("Press keys (press 'n' for next device, 'r' to retry, 'q' to exit):")

    while True:
        char = key_reader.getch()

        # quit
        if char == "q":
            print("\nQuitting...")
            KEEP_GOING = False
            break

        # retry
        elif char == "r":
            break

        elif char == "n":
            config["hardware_id"] += 1
            save_config(config)
            break


def main():
    # Check environment, do you have the configuration.json file?
    # Check if you have the firmware files?
    print("ESP NIC Tool Flasher")
    input("\nPress enter to continue...")
    while KEEP_GOING:
        generate_eeprom()
        flash()
        post_flashing()
        clear_screen()


if __name__ == "__main__":
    main()
