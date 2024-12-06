import os

import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.display as display

def install_update_gateway_updater():
    display.output_message("Installing/updating gateway updater...", status='info')
    # Uninstall lumeo-container-update cron script if installed
    if os.path.exists("/etc/cron.hourly/lumeo-container-update"):
        hostutils.run_command("rm -f /etc/cron.hourly/lumeo-container-update", sudo=True)
        display.output_message("Removed old lumeo-container-update cron script", status='info')

    # Uninstall lumeo-wgm-update cron script if installed
    if os.path.exists("/etc/cron.hourly/lumeo-wgm-update-cron"):
        hostutils.run_command("rm -f /etc/cron.hourly/lumeo-wgm-update-cron", sudo=True)
        display.output_message("Removed old lumeo-wgm-update-cron cron script", status='info')

    # Install the new, unified lumeo-update-cron.sh script
    new_update_script_name = "lumeo-gateway-update" # TODO: rename to lumeo-update-cron when we start publishing to the web
    if not os.path.exists(f"/etc/cron.hourly/{new_update_script_name}"):    
        script_path = os.path.join(os.path.dirname(__file__), f"{new_update_script_name}.sh")
        hostutils.run_command(f"install -m u=rwx,g=rx,o=rx {script_path} /etc/cron.hourly/{new_update_script_name}", sudo=True)