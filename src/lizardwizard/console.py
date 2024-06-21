import sys
from cloudmesh.common.console import Console
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import readfile, writefile, path_expand
from cloudmesh.common.systeminfo import os_is_windows, os_is_mac
from docopt import docopt
import pygetwindow as gw
import subprocess
import re


def main():
    doc = """
Welcome to the greatest lizard wizard ever
Did you know that you are swag?
Thanks.

Usage:
    lw stop
    lw shutdown
    lw down
    lw choco
    lw nat
    lw help

Commands:
    stop      shutdown reptilian
    shutdown  shutdown reptilian
    down      shutdown reptilian
    choco     automatically install chocolatey
    nat       setup ssh config
    help      Show this help message
    """

    if len(sys.argv) < 2 or sys.argv[1] in ['help', 'hello', 'hi']:
        print(doc)
        return

    args = docopt(doc, version='1.0')

    if args['choco']:
        
        Shell.install_chocolatey()
        Shell.install_choco_package('git.install --params "/GitAndUnixToolsOnPath /Editor:Nano /PseudoConsoleSupport /NoAutoCrlf"')
        script = """
env=~/.ssh/agent.env

agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

agent_start () {
    (umask 077; ssh-agent >| "$env")
    . "$env" >| /dev/null ; }

agent_load_env

# agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2=agent not running
agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
    agent_start
    ssh-add
elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
    ssh-add
fi

unset env
        """
        expanded = path_expand('~/.bashrc')
        writefile(expanded, script)
        Console.ok("bashrc should be written")

    if args['nat']:
        configfile = """
Host reptilian
    User reptilian
    HostName 127.0.0.1
    Port 3022
    IdentityFile ~/.ssh/id_rsa
        """
        # append to the file.
        config_path = path_expand("~/.ssh/config")
        with open(config_path, 'a') as f:
            f.write(configfile)
        Console.ok("ssh config should be written")

    if args['stop'] or args['shutdown'] or args['down']:
        if os_is_windows():

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
                quit()

        elif os_is_mac():
            r = Shell.run("cd /Applications/VirtualBox.app/Contents/MacOS ; ./VBoxManage list runningvms")
            
            match = re.search(r'"(.*?)"', r)
            if match:
                name = match.group(1)
            else:
                Console.error("No VM running!")
                quit()
            
            bash_script = f"""
            # Set the VM name
            vmName="{name}"
            
            # VBoxManage dir
            cd "/Applications/VirtualBox.app/Contents/MacOS"
            
            # Enter (wake machine)
            ./VBoxManage controlvm "$vmName" keyboardputscancode 1c 9c
            
            # Wait for 2 seconds
            sleep 2
            
            # Send CTRL+ALT+DEL
            ./VBoxManage controlvm "$vmName" keyboardputscancode 1d 38 53 9d b8 d3
            
            # Wait for 4 seconds
            sleep 4
            
            # Send Tab (select shutdown)
            ./VBoxManage controlvm "$vmName" keyboardputscancode 0f 8f
            
            # Wait for 2 seconds
            sleep 2
            
            # Send Enter (shutdown)
            ./VBoxManage controlvm "$vmName" keyboardputscancode 1c 9c
            """
            subprocess.run(["/bin/bash", "-c", bash_script], check=True)


if __name__ == "__main__":
    main()
