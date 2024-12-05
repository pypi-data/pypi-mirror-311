

from machineconfig.utils.utils import PROGRAM_PATH
from crocodile.file_management import P
import platform


def main():
    print("Welcome to the WindowsNetworkDrive Mounting Wizard")
    drive_location = input("Enter the network drive location (ex: //192.168.1.100/Share): ")
    machine_name = drive_location.split("//")[1].split("/")[0]
    mount_point = input(f"Enter the mount point directory (ex: /mnt/network) [default: ~/data/mount_nw/{machine_name}]: ")
    if mount_point == "": mount_point = P.home().joinpath(fr"data/mount_nw/{machine_name}")
    else: mount_point = P(mount_point).expanduser()

    username = input("Enter the username: ")
    password = input("Enter the password: ")
    if platform.system() == "Linux":
        PROGRAM_PATH.write_text(f"""
drive_location='{drive_location}'
mount_point='{mount_point}'
username='{username}'
password='{password}'

""")
    elif platform.system() == "Windows":
        raise NotImplementedError


if __name__ == '__main__':
    main()
