import os
import platform
import yaml
import requests
from pathlib import Path

import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.common as common
import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.updater as updater
import lumeo.scripts.gateway.docker as dockerutils
import lumeo.scripts.gateway.lumeod as lumeod

def get_wgm_status():
    """Get the status of the Lumeo Web Gateway Manager."""
    status = "not_installed"
    status_str = "Web Gateway Manager: "
    containers = dockerutils.DOCKER_CLIENT.containers.list(all=True, filters={"name": "lumeo_wgm"})
    if containers:
        status = containers[0].status
        container_info = containers[0].attrs        
        status_str += f"{container_info['Name']} ({container_info['Config']['Image']})"
        if status == "running":
            status_str += f" [bold green]{status.capitalize()}[/bold green]"
        else:
            status_str += f" [bold red]{status.capitalize()}[/bold red]"
    else:
        status_str += "[orange]Not Installed[/orange]"
    return status, status_str


def install_wgm():
    """Install Lumeo Web Gateway Manager."""   
    
    display.output_message("Installing Lumeo Web Gateway Manager...", status='info')    
     
    arch_type = platform.machine()
    
    wgm_status, _ = get_wgm_status()
    
    if wgm_status == 'not_installed':
        common.install_common_dependencies()
            
        # Create shared volume directory
        os.makedirs("/opt/lumeo/wgm", exist_ok=True)    
        
        # Install WGM container
        wgm_container = "lumeo/wgm-x64:latest" if arch_type == "x86_64" else "lumeo/wgm-arm:latest"

        # Remove existing lumeo_wgm container
        if hostutils.run_command("docker ps -a -q -f name=lumeo_wgm", sudo=True, check=False):
            hostutils.run_command("docker stop lumeo_wgm", sudo=True)
            hostutils.run_command("docker rm lumeo_wgm", sudo=True)
            hostutils.run_command("rm -rf /opt/lumeo/wgm", sudo=True)

        # Pull and run new container
        #run_command(f"docker pull {wgm_container}", sudo=True)
        dockerutils.docker_download_image(wgm_container)
        hostutils.run_command(f"docker run -d -v /opt/lumeo/wgm/:/lumeo_wgm/ --name lumeo_wgm --restart=always --network host {wgm_container}", sudo=True)

        # Install and start lumeo-wgm-pipe
        hostutils.run_command("install -m u=rw,g=r,o=r /opt/lumeo/wgm/scripts/lumeo-wgm-pipe.service /etc/systemd/system/", sudo=True)
        hostutils.run_command("systemctl enable --now lumeo-wgm-pipe", sudo=True)

        # Restart container
        hostutils.run_command("docker restart lumeo_wgm", sudo=True)

        # Install update cron job
        updater.install_update_gateway_updater()

        display.output_message("Lumeo Web Gateway Manager has been installed. Access by visiting https://<device-ip-address>", status='info')
    else:
        display.output_message("Lumeo Web Gateway Manager is already installed.", status='info')
    
    return


def update_wgm():
    """Update Lumeo Web Gateway Manager."""        
    
    display.output_message("Updating Lumeo Web Gateway Manager...", status='info')
    
    # Determine the appropriate container based on architecture
    arch_type = platform.machine()
    wgm_container = "lumeo/wgm-x64:latest" if arch_type == "x86_64" else "lumeo/wgm-arm:latest"

    # Get the Image ID of the currently running container
    running_image_id = hostutils.run_command("docker inspect --format='{{.Image}}' lumeo_wgm", sudo=True)

    if running_image_id:
        # Pull the latest image
        #run_command(f"docker pull {wgm_container}", sudo=True)
        dockerutils.docker_download_image(wgm_container)

        # Get the Image ID of the latest image
        latest_image_id = hostutils.run_command(f"docker inspect --format='{{{{.Id}}}}' {wgm_container}", sudo=True)

        # Compare the IDs. If they are different, stop, remove and run the new container
        if running_image_id != latest_image_id:
            hostutils.run_command("docker stop lumeo_wgm && docker rm -f lumeo_wgm", sudo=True)

            # Host network needed for bonjour broadcast
            hostutils.run_command(f"docker run -d -v /opt/lumeo/wgm/:/lumeo_wgm/ --name lumeo_wgm --restart=always --network host {wgm_container}", sudo=True)
            hostutils.run_command("systemctl restart lumeo-wgm-pipe", sudo=True)
            
            # Remove the old image
            hostutils.run_command(f"docker image rm -f {running_image_id}", sudo=True)
            display.output_message("Updated and started new WGM container successfully.", status='info')
        else:
            display.output_message("Running WGM container is up-to-date.", status='info')
            
        updater.install_update_gateway_updater()
    else:
        display.output_message("Lumeo Web Gateway Manager container not found.", status='warning')
    
    return

def remove_wgm():
    """Remove Lumeo Web Gateway Manager."""
    wgm_status, _ = get_wgm_status()
    display.output_message("Removing Lumeo Web Gateway Manager...", status='info')
    
    if wgm_status != 'not_installed':
        # Stop and remove container
        hostutils.run_command("docker stop lumeo_wgm && docker rm -f lumeo_wgm", sudo=True, check=False)
        # Remove MediaMTX container if it exists
        hostutils.run_command("docker stop mediamtx && docker rm -f mediamtx", sudo=True, check=False)
        # Remove lumeo-wgm-pipe service
        hostutils.run_command("systemctl stop lumeo-wgm-pipe", sudo=True, check=False)
        hostutils.run_command("systemctl disable lumeo-wgm-pipe", sudo=True, check=False)
        hostutils.run_command("rm /etc/systemd/system/lumeo-wgm-pipe.service", sudo=True, check=False)
        hostutils.run_command("systemctl daemon-reload", sudo=True, check=False)
        # Remove shared volume directory
        hostutils.run_command("rm -rf /opt/lumeo/wgm", sudo=True, check=False)
        display.output_message("Lumeo Web Gateway Manager has been removed.", status='info')
    else:
        display.output_message("Lumeo Web Gateway Manager is not installed.", status='info')
    
    return

def reset_wgm(silent=False):
    """Reset the password for the Lumeo Web Gateway Manager."""    
    reset = True
    
    if not silent:
        display.print_header("Lumeo Web Gateway Manager Password Reset")
        display.output_message("[bold red]Resetting the web password will require you to create a new device account via the web interface. "
                       "You should do so immediately, since once reset, anyone can create a new device account.[/bold red]")
        reset = display.prompt_yes_no("Would you like to reset the web password for this device?", "y")
    
    if reset:
        hostutils.run_command("rm -f /opt/lumeo/wgm/db.sqlite", sudo=True)
        hostutils.run_command("docker restart lumeo_wgm", sudo=True)
        display.output_message("Web gateway manager account reset complete", status='info')


def oem_install():
    
    oem_config_file = os.getenv("OEM_CONFIG_FILE", None)
    
    """Install Lumeo Gateway and Web Gateway Manager with OEM configuration."""
    display.print_header("This script is intended for OEMs to use. It will:\n"
                        "1. download the latest Lumeo Gateway Container image\n"
                        "2. install Lumeo Web Gateway Manager that advertises this device "
                        "over the network and allows it to be configured using a web interface.\n"
                        "3. Applies OEM branding\n"
                        "4. Optionally Seals the device\n"
                        "After installation, access web interfaceby visiting https://<device-ip-address>", title="Lumeo OEM Installation")
    
    display.output_message("Installing Lumeo Gateway and Web Gateway Manager with OEM configuration...", status='info')
    
    # Download the latest lumeod container if not already present
    lumeo_containers = lumeod.get_lumeo_containers()
    if not lumeo_containers:
        lumeod.download_container()
    else:
        display.output_message("Lumeo Gateway container already installed. Skipping image download.", status='info')
    
    # Install WGM
    wgm_status, _ = get_wgm_status()
    if wgm_status == 'not_installed':
        install_wgm()
    else:
        update_wgm()
    
    # Apply OEM configuration
    apply_oem_config(oem_config_file)
    
    # Seal the device
    seal_device(default='y')
    
    return


def apply_oem_config(oem_config_file=None):
    """Apply OEM configuration from a YAML file."""

    if not oem_config_file:
        return

    display.output_message("Customizing OEM Branding", status='info')
        
    if not os.path.isfile(oem_config_file):
        display.output_message(f"File {oem_config_file} does not exist", status='error')
        return

    wgm_oem_config_path = "/opt/lumeo/wgm/"
    oem_config_file_name = "oemconfig.yaml"
    display.output_message(f"Copying file {oem_config_file} to {wgm_oem_config_path}/{oem_config_file_name}", status='info')
    hostutils.run_command(f"cp {oem_config_file} {wgm_oem_config_path}/{oem_config_file_name}", sudo=True)

    if not os.path.isfile(wgm_oem_config_path + oem_config_file_name):
        display.output_message(f"Failed to copy {oem_config_file} to {wgm_oem_config_path}", status='error')
        return

    with open(wgm_oem_config_path + oem_config_file_name, 'r') as f:
        config = yaml.safe_load(f)

    for logo_type in ['logoUrl', 'oemLogoUrl']:
        if logo_type in config:
            url = config[logo_type].strip()
            if url:
                display.output_message(f"Downloading logo from {url} ...", status='info')
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    logo_filename = 'logo.png' if logo_type == 'logoUrl' else 'oemlogo.png'
                    logo_path = wgm_oem_config_path + logo_filename
                    with open(logo_path, 'wb') as f:
                        f.write(response.content)
                    display.output_message(f"Logo saved to {logo_path}", status='info')
                except requests.RequestException as e:
                    display.output_message(f"Error downloading logo from {url}: {str(e)}. Skipping...", status='error')

    display.output_message("Restarting Docker to apply OEM Branding", status='info')
    hostutils.run_command("docker restart lumeo_wgm", sudo=True)    
    return


def seal_device(default='n'):
    """Seal the device."""
    display.output_message("Sealing the device...", status='info')
    
    if not display.prompt_yes_no("Do you want to seal the device? This will stop existing lumeod containers so users can link their own, "
                                 "reset web login/password, and (OPTIONALLY) turn off ssh access and local user password.", default):
        display.output_message("Device sealing cancelled.", status='info')
        return

    reset_wgm(silent=True)

    dockerutils.stop_and_remove_docker_containers("lumeo/gateway")

    hostutils.toggle_ssh(enable=False)

    local_user = 'lumeo'
    oem_config_path = "/opt/lumeo/wgm/oemconfig.yaml"
    if os.path.isfile(oem_config_path):
        with open(oem_config_path, 'r') as f:
            oem_config = yaml.safe_load(f)
            local_user = oem_config.get('localUser', 'lumeo').strip()

    hostutils.toggle_user_lock(local_user, lock=True)

    display.output_message("Device sealing complete.", status='success')