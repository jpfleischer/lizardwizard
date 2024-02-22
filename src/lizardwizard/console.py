import sys
from cloudmesh.common.console import Console
from docopt import docopt
import pygetwindow as gw
import subprocess

def main():
    doc = """
Welcome to the greatest lizard wizard ever
Did you know that you are swag?
Thanks.

Usage:
    lw stop
    lw shutdown
    lw down
    lw help

Commands:
    stop      shutdown reptilian
    shutdown  shutdown reptilian
    down      shutdown reptilian
    help      Show this help message
    """

    if len(sys.argv) < 2 or sys.argv[1] in ['help', 'hello', 'hi']:
        print(doc)
        return

    args = docopt(doc, version='1.0')

    if args['stop'] or args['shutdown'] or args['down']:
        windows = gw.getAllTitles()
        running = any('Oracle VM VirtualBox' in title for title in windows)
        if running:
            # Find the window with 'Oracle VM VirtualBox' in the title, excluding 'Oracle VM VirtualBox Manager'
            vm_window = next((title for title in windows if 'Oracle VM VirtualBox' in title and title != 'Oracle VM VirtualBox Manager'), None)

            if vm_window is not None:
                # Find the first instance of " (" and use everything before it as the VM name
                vm_name = vm_window.split(" (", 1)[0]

                Console.info(f"Shutting down {vm_name}...")

                powershell_script = fr"""
                # Set the VM name
                $vmName = "{vm_name}"
                
                # VBoxManage dir
                cd "C:\Program Files\Oracle\VirtualBox"
                
                # Enter (wake machine)
                .\VBoxManage controlvm $vmName keyboardputscancode 1c 9c
                
                # Wait for 2 seconds
                Start-Sleep -Seconds 2
                
                # Send CTRL+ALT+DEL
                .\VBoxManage controlvm $vmName keyboardputscancode 1d 38 53 9d b8 d3
                
                # Wait for 4 seconds
                Start-Sleep -Seconds 4
                
                # Send Tab (select shutdown)
                .\VBoxManage controlvm $vmName keyboardputscancode 0f 8f
                
                # Wait for 2 seconds
                Start-Sleep -Seconds 2
                
                # Send Enter (shutdown)
                .\VBoxManage controlvm $vmName keyboardputscancode 1c 9c
                """
                subprocess.run(["powershell", "-Command", powershell_script], check=True)
        else:
            Console.error("No VM running!")

if __name__ == "__main__":
    main()