import argparse
import os
import requests
from zipfile import ZipFile
import subprocess
import shutil
import time
from aacommpy.nugetmanagement import download_nuget, nuget_version, update_nuget, dotnetfw, check_dotnet_versions
from settings import NET_FRAMEWORK_CHOICES


entry_points = {
    'console_scripts': [
        'nuget_download = nugetmanagement:download_nuget',
        'nuget_version = nugetmanagement:nuget_version',
        'update_nuget = nugetmanagement:update_nuget'
    ]
}
def install_template() -> None:
    msg = 'Download Python package for AAComm to this directory (y/n)? '
    user_response = input(msg)
    if user_response != 'y':
        return None

    directory = os.path.join(os.path.dirname(__file__), 'aacommpyDownloader-main')
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    url = 'https://dist.nuget.org/win-x86-commandline/latest/nuget.exe'
    r = requests.get(url)
    with open(os.path.join(directory, 'nuget.exe'), 'wb') as f:
        f.write(r.content)

    return None

def download_and_install(version: str = "") -> None:
    install_template()
    # Add code to wait for the nuget.exe file to be fully downloaded
    nuget_path = os.path.join(os.path.dirname(__file__), 'aacommpyDownloader-main', 'nuget.exe')
    while not os.path.exists(nuget_path):
        time.sleep(1)
    # nuget.exe is fully downloaded, proceed with download_nuget()
    if version != "":
        download_nuget(version)
    else:
        download_nuget()
    # Perform additional actions after download_nuget()
    available_versions = check_dotnet_versions()
    if available_versions is not None and len(available_versions) > 0:
        dotnetfw(available_versions[0])
    return None

def main() -> None:
    parser = argparse.ArgumentParser(description='Download aacommpy package.')
    parser.add_argument('command', choices=['install', 'downloadnuget', 'version', 'update', 'dotnetfw'], help='Choose a command to execute.')
    parser.add_argument('--version', help='Specify version to install/download.')
    parser.add_argument('--netfw', choices=NET_FRAMEWORK_CHOICES, default='net40', help='Choose the .NET framework version to use.')
    parser.add_argument('--check', action='store_true', help='Check compatibility versions of .NET framework.')
    args = parser.parse_args()

    if args.command == 'install':
        if args.version:
            download_and_install(args.version)
        else:
            download_and_install()
    elif args.command == 'version':
        nuget_version()
    elif args.command == 'update':
        update_nuget()
    elif args.command == 'dotnetfw':
        if args.check:
            check_dotnet_versions()
        else:
            dotnetfw(version=args.netfw)
    else:
        raise RuntimeError('Please supply a valid command for aacommpy - e.g. install.')

    return None

if __name__ == '__main__':
    main()
