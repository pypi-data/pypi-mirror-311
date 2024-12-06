import os
import subprocess
import sys
import time

import lumeo.scripts.gateway.display as display

# Common host utilities
def check_os():
    """Check if the OS is Linux."""
    if os.name != "posix" or os.uname().sysname != "Linux":
        display.output_message("[check_os] This script must be run on a Linux system.", status='error')
        sys.exit(1)


def check_command(command, sudo=False, silent=False):
    """Check if a command exists."""
    command_name = command.split()[0]  # Get the name of the command
    check_command = f"{'sudo ' if sudo else ''}which {command_name} > /dev/null 2>&1"
    exists = (os.system(check_command) == 0)
    if not exists and not silent:
        display.output_message(f"[check_command] Command '{command}' not found.", status='error')
    return exists


def run_command(command, check=True, shell=True, sudo=False, error_message=None, useOsRun=False, silent=False):
    """Run a command and return its output."""
    try:        
        if not check_command(command, sudo, silent):
            return None
        
        if sudo:
            command = f"sudo {command}"
        
        if not shell:
            command = command.split()
            
        if useOsRun:
            result = os.system(command)
            return result
        else:
            result = subprocess.run(command, check=check, shell=shell, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        display.output_message(f"run_command: Error executing command: {e}", status='error')
        display.output_message(f"run_command: Command output: {e.output}", status='error')
        display.output_message(f"run_command: Command error: {e.stderr}", status='error')
        if error_message:
            display.output_message(f"run_command: {error_message}", status='error')
        sys.exit(1)

def check_lock(command):
    """Check for apt/dpkg locks and wait if necessary."""
    max_attempts = 300
    display.get_progress(reset=True)
    display.add_progress_task("check_lock", f"Waiting for locks to be released...", total=max_attempts)    

    for i in range(max_attempts):
        if not run_command("sudo fuser /var/lib/dpkg/lock /var/lib/apt/lists/lock /var/cache/apt/archives/lock", check=False):
            break
        display.update_progress_task("check_lock", advance=1)
        time.sleep(1)
    else:
        display.output_message("[check_lock] Unable to acquire lock after 5 minutes. Aborting installation.", status='error')
        sys.exit(1)
    
    display.update_progress_task("check_lock", completed=max_attempts)
    display.stop_progress()
    
    run_command(command, shell=True, sudo=True)

def apt_install(packages, update_first=False):
    """Install packages using apt, optionally updating first."""
    if update_first:
        check_lock("apt -qq update")
    check_lock(f"apt -qq install -y {packages}")


# Install host packages
def setup_host_common():
    display.output_message("Installing host common dependencies...", status='info')
    apt_install("curl jq python3 lshw util-linux smartmontools gnupg", update_first=True)


def prompt_disable_x_server_default_yes():
    return prompt_disable_x_server(default='y')


def prompt_disable_x_server(default='n'):
    """Prompt to disable X server and return whether a reboot is required."""
    if display.prompt_yes_no("[Optional] Disable GUI (X server) to free up memory, allowing you to run more pipelines? (reboot required)", default):
        #run_command("systemctl enable multi-user.target", sudo=True)
        run_command("systemctl set-default multi-user.target", sudo=True)
        display.output_message("GUI (X server) disabled. In order to take effect, a reboot is required. Remember to reboot after installation.", status='info')
        return True
    return False


def toggle_ssh(enable=False):
    """Enable or disable SSH."""
    action = "enable" if enable else "disable"
    if display.prompt_yes_no(f"Do you want to {action} SSH?", "n"):
        display.output_message(f"toggle_ssh: {'Enabling' if enable else 'Disabling'} SSH...", status='info')
        run_command(f"systemctl {action} ssh", sudo=True)
        display.output_message(f"toggle_ssh: SSH has been {action}d.", status='info')
    else:
        display.output_message(f"toggle_ssh: SSH {action} cancelled.", status='info')


def toggle_user_lock(username, lock=True):
    """Lock or unlock the user account."""    
    action = "lock" if lock else "unlock"
    if display.prompt_yes_no(f"Do you want to {action} the password for user {username}?", "n"):
        display.output_message(f"toggle_user_lock: {'Locking' if lock else 'Unlocking'} password for user {username}...", status='info')
        run_command(f"passwd -{action[0]} {username}", sudo=True)
        display.output_message(f"toggle_user_lock: User {username} has been {action}ed.", status='info')
    else:
        display.output_message(f"toggle_user_lock: User {username} {action} cancelled.", status='info')
        

def check_disk_space():
    docker_data_folder = run_command("docker info -f '{{ .DockerRootDir}}'", sudo=True)
    if os.path.isdir(docker_data_folder):
        arch_type = os.uname().machine
        required_size_KB = 8388608 if arch_type == "aarch64" else 20971520

        available_space_KB = int(run_command(f"df -P {docker_data_folder} | awk 'END{{print $4}}'", sudo=True))

        if available_space_KB < required_size_KB:
            required_size_GB = required_size_KB / (1024 ** 2)
            available_space_GB = available_space_KB / (1024 ** 2)

            display.output_message("WARNING: There is not enough free space on the disk where Docker stores its data."
                           f"You have {available_space_GB:.2f} GB available, but at least {required_size_GB:.2f} GB is required for fresh lumeod installations."
                           "If the container image has not been pulled yet, or lumeod is not installed, you might run out of disk space during installation.", 
                           status='warning')

            if display.prompt_yes_no("Do you want to continue despite the low disk space?", "n"):
                display.output_message("Proceeding despite the low disk space warning.", status='warning')
            else:
                display.output_message("Exiting due to insufficient disk space.", status='error')
                exit(1)


def ensure_directory_with_permissions(path, permissions=0o777):
    """
    Ensures the directory exists and sets the specified permissions.
    :param path: The directory path to create or modify.
    :param permissions: The permission to apply (default is 0o777).
    :return: True if successful, False if an error occurred.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            os.chmod(path, permissions)
            display.output_message(f"Directory {path} created and permissions set to {oct(permissions)}.", "debug")
        except Exception as e:
            display.output_message(f"Failed to create directory {path}: {str(e)}", "error")
            return False
    else:
        try:
            os.chmod(path, permissions)
            display.output_message(f"Permissions set for existing directory {path} to {oct(permissions)}.", "debug")
        except Exception as e:
            display.output_message(f"Failed to set permissions for directory {path}: {str(e)}", "error")
            return False
    return True
