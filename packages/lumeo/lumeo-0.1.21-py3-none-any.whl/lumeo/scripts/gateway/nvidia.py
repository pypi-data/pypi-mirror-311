import os
import sys
import platform
import requests
import filecmp
import glob

import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.hostutils as hostutils

def check_nvidia_dgpu_driver():
    """Check if the NVIDIA driver is installed and up to date."""
    MIN_NVIDIA_DRIVER_VERSION = 515
    
    arch_type = platform.machine()
    if arch_type == "x86_64":
        if not hostutils.check_command("nvidia-smi", silent=True):
            display.output_message("Error: Can't find nvidia-smi. Lumeo container requires an NVIDIA GPU and corresponding drivers.", status='error')
            sys.exit(1)

        # Check nvidia-smi output and return error if command fails
        hostutils.run_command("nvidia-smi", check=False, error_message="nvidia-smi returned an error. Please check the output below for more information:")

        driver_version = get_dgpu_driver_version()
        if driver_version < MIN_NVIDIA_DRIVER_VERSION:
            display.output_message(f"NVIDIA dGPU driver is outdated: {driver_version}.", status='error')
            display.output_message(f"Please upgrade NVIDIA driver to {MIN_NVIDIA_DRIVER_VERSION} or higher.", status='error')
            sys.exit(1)    
            
def check_disable_nvidia_driver_updates():
    """Disable NVIDIA GPU driver updates by apt if user chooses to."""
    arch_type = platform.machine()
    if arch_type == "x86_64":
        installed_nvidia_driver_package = hostutils.run_command("dpkg -l | grep nvidia-driver | awk '/ii/{print $2}'", check=False)
        held_nvidia_driver_package = hostutils.run_command("dpkg -l | grep nvidia-driver | awk '/hi/{print $2}'", check=False)
        if installed_nvidia_driver_package:
            if display.prompt_yes_no("Disable NVIDIA GPU drivers update by apt?", "n"):
                hostutils.run_command(f"apt-mark hold {installed_nvidia_driver_package}", sudo=True)
                display.output_message(f"NVIDIA driver package {installed_nvidia_driver_package} has been held from updates.", status='info')
        elif not held_nvidia_driver_package:
            display.output_message("NVIDIA driver package not found. Unable to hold the package.", status='error')
        else:
            display.output_message(f"NVIDIA driver package {held_nvidia_driver_package} found. Held from updates.", status='info')

def get_dgpu_driver_version():
    version_string = hostutils.run_command('nvidia-smi --query-gpu=driver_version --format=csv,noheader', check=False)
    return int(version_string.split('.')[0])



#################################################
# Jetson specific functions
#################################################

def l4t_version():
    """Get the installed Jetpack L4T version."""
    try:
        result = hostutils.run_command("apt-cache policy nvidia-l4t-core")
        for line in result.splitlines():
            if "Installed:" in line:
                return line.split()[1]
    except Exception:
        return None
    return None


def install_jetson_extras():
    arch_type = os.uname().machine
    if arch_type == "aarch64":
        l4t_ver = l4t_version()
        if l4t_ver and l4t_ver >= "36":
            hostutils.apt_install("nvidia-l4t-dla-compiler "
                        "nvidia-l4t-jetson-multimedia-api "
                        "nvidia-l4t-gstreamer "
                        "gstreamer1.0-plugins-good "
                        "gstreamer1.0-plugins-bad "
                        "gstreamer1.0-plugins-ugly "
                        "gstreamer1.0-libav",
                        update_first=True)    
    

def enable_jetson_clocks():
    """Enable Jetson clocks and set power mode for specific Jetson devices."""
    arch_type = platform.machine()    
    if arch_type == "aarch64":
        jetson_codename = os.getenv('JETSON_CODENAME')
        if jetson_codename and jetson_codename in ['galen', 'jakku']:
            jetson_target_power_mode = "0" if jetson_codename == "galen" else "8"
            hostutils.run_command(f"nvpmodel -m {jetson_target_power_mode}", sudo=True)
            hostutils.run_command("rm -rf /var/lib/nvpmodel/status", sudo=True)
            hostutils.run_command(f"sed -i -e 's/\\(< PM_CONFIG DEFAULT=\\).*\\( >\\)/< PM_CONFIG DEFAULT={jetson_target_power_mode} >/g' /etc/nvpmodel.conf", sudo=True)

        jetson_clocks_file = "/tmp/jetson_clocks.service"
        response = requests.get("https://assets.lumeo.com/lumeod/jetson_clocks.service")
        with open(jetson_clocks_file, 'wb') as file:
            file.write(response.content)
        
        hostutils.run_command(f"install -m u=rw,g=r,o=r {jetson_clocks_file} /etc/systemd/system/", sudo=True)
        hostutils.run_command("systemctl start jetson_clocks", sudo=True)
        hostutils.run_command(f"rm {jetson_clocks_file}", sudo=True)
    
    
def get_jetson_model_name():
    arch_type = platform.machine()
    if arch_type == "aarch64":
        try:
            import Jetson.GPIO as GPIO
            jetson_model_name = str(GPIO.model)                
            return jetson_model_name
        except:
            pass            
    return None


def setup_jetson_gpio():
    if get_jetson_model_name():
        # Copy udev rules for GPIO chip.
        import Jetson.GPIO as GPIO
        package_path = os.path.dirname(GPIO.__file__)
        source_path = os.path.join(package_path, '99-gpio.rules')
        destination_path = "/etc/udev/rules.d/99-gpio.rules"
        if (os.path.exists(source_path) and \
            (not os.path.exists(destination_path) or not filecmp.cmp(source_path, destination_path))):
            hostutils.run_command(f"cp {source_path} {destination_path}", sudo=True)
            hostutils.run_command(["udevadm", "control", "--reload-rules"], check=True)
            hostutils.run_command(["udevadm", "trigger", "--action=add"], check=True)    
            
            


#################################################
# Common functions
#################################################

def get_nvidia_docker_runtime():
    arch_type = platform.machine()
    if arch_type == "aarch64":
        if l4t_version() < "35.1":
            return None
        else:
            # "nvidia" runtime is required starting from JetPack 5.0.
            return "nvidia"
    elif arch_type == "x86_64":
        return None
    else:
        raise RuntimeError("Unsupported platform: {}".format(arch_type))
    
def get_devices_for_container():
    gpio = glob.glob("/dev/gpiochip*") if get_jetson_model_name() else []
    all = get_usb_cameras() + gpio
    return all or None

def get_usb_cameras():
    usb_cameras_list = []
    try:
        list_of_cameras = hostutils.run_command("ls /dev/video* -R 2>/dev/null", check=False).split()
        for usb_cam in list_of_cameras:
            usb_cameras_list.append("{}:{}:rwm".format(usb_cam, usb_cam))
    except:
        pass

    return usb_cameras_list
 