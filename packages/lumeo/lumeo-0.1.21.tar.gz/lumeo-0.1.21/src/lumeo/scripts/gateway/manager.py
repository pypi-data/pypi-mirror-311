import argparse
import os
import sys

from lumeo.utils import check_for_update
import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.lumeod as lumeod
import lumeo.scripts.gateway.wgm as wgm
import lumeo.scripts.gateway.schedule as schedule
import lumeo.scripts.gateway.docker as dockerutils
import lumeo.scripts.gateway.hostutils as hostutils

def exit_manager():
    sys.exit(0)
    
COMMANDS = {
    "list": ("List the currently installed Lumeo gateway containers", lumeod.list_containers, True),
    "install": ("Install a new Lumeo gateway container", lumeod.install_container, True),
    "download": ("Download the latest Lumeo gateway container image (OEM use only)", lumeod.download_container, True),
    "stop": ("Kills a running Lumeo gateway container", lumeod.stop_container, True),
    "restart": ("Restart a Lumeo gateway container & update to the latest version", lumeod.upgrade_and_restart_container, True),
    "update": ("Update all Lumeo gateway containers to the latest image", lumeod.update_containers, True),
    "remove": ("Remove a Lumeo gateway container", lumeod.remove_container, True),
    "logs": ("Print the logs of a Lumeo gateway container", lumeod.logs, True),
    "shell": ("Open an interactive shell in a running Lumeo gateway container", lumeod.shell, True),

    "schedule": ("Schedule container update in a certain date range", schedule.edit_update_schedule, True),
    
    "install-wgm": ("Install Web Gateway Manager", wgm.install_wgm, True),
    "update-wgm": ("Update Web Gateway Manager", wgm.update_wgm, True),
    "reset-wgm": ("Reset Web Gateway Manager", wgm.reset_wgm, True),
    "remove-wgm": ("Remove Web Gateway Manager", wgm.remove_wgm, True),
    
    "install-oem": ("Download Lumeo Gateway image and install Web Gateway Manager with OEM configuration", wgm.oem_install, True),
    
    "fix_nvidia_driver_issue": ("Fix the issue with the NVIDIA driver", dockerutils.fix_nvidia_nvml_init_issue, False),
    "set_docker_logs_configuration": ("Set the Docker logs configuration", dockerutils.set_docker_logs_configuration, False),
    "write_hardware_information": ("Write the hardware information to a file", lumeod.write_hardware_information_to_container, False),    
    "start_watchtower": ("Start Watchtower", dockerutils.start_watchtower, False),
    "migrate_watchtower": ("Migrate Watchtower", dockerutils.migrate_watchtower, False),
    "disable_x_server": ("Disable X server", hostutils.prompt_disable_x_server_default_yes, False),
    
    "exit": ("Quits this script", exit_manager, True),
}

def print_menu():
    update_info = check_for_update()
    _, wgm_status_str = wgm.get_wgm_status()
    lumeo_containers_all = lumeod.get_lumeo_containers(show_all=True)
    lumeo_containers_running = lumeod.get_lumeo_containers(show_all=False)
    subtitle = f"Status | Lumeo Gateways: [bold green]{len(lumeo_containers_running)} running[/bold green], [bold]{len(lumeo_containers_all)} total[/bold] | {wgm_status_str}"
    print('')
    display.print_header(get_commands(), f"[bold red]BETA[/bold red] [bold cyan]Lumeo Gateway Manager v{update_info[2]}[/bold cyan]", subtitle=subtitle)

def get_commands():
    headers = ["Command", "Description"]
    rows = [
        [command_name, description]
        for command_name, (description, _, show_in_menu) in COMMANDS.items()
        if show_in_menu
    ]
    return display.generate_table(headers, rows, "Commands", expand=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=COMMANDS.keys(), nargs="?")
    parser.add_argument("--container-name")
    parser.add_argument("--force-update", action="store_true", help="Force update without checking schedule")
    parser.add_argument("--no-prompt", action="store_true", help="Script mode. Uses defaults, does not prompt for input", default=False)
    parser.add_argument("--app-id", help="Lumeo workspace / app id to link a gateway to")
    parser.add_argument("--api-key", help="Lumeo workspace/app API key")
    parser.add_argument("--gateway-name", help="Gateway name to be used for a new `install` with `--no-prompt` options.")
    parser.add_argument("--replace-schedule", help="Replace the existing update schedule with a new one, to be used with `schedule` + `--no-prompt` option.")
    parser.add_argument("--oem-config-file", help="Optional OEM configuration file to be used for a `install-oem` option.")
    parser.add_argument("--media-volume-path", help="Optional host media volume path to be used with `install` or `restart` options. Must be an absolute path or 'remove' to remove an existing mapping.")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    
    if args.debug:
        display.set_debug_mode(True)    
    if args.no_prompt:
        os.environ['NO_PROMPT'] = 'true'
    if args.app_id:
        os.environ['LUMEO_APP_ID'] = args.app_id
    if args.api_key:
        os.environ['LUMEO_API_KEY'] = args.api_key
    if args.gateway_name:
        os.environ['LUMEO_GATEWAY_NAME'] = args.gateway_name
    if args.json:  
        display.set_output_format(args.json)
        os.environ['NO_PROMPT'] = 'true'
    if args.oem_config_file:
        os.environ['OEM_CONFIG_FILE'] = args.oem_config_file
    if args.replace_schedule:
        os.environ['LUMEO_UPDATE_SCHEDULE'] = args.replace_schedule
    if args.media_volume_path:
        os.environ['LUMEO_MEDIA_VOLUME_PATH'] = args.media_volume_path

    if not args.command:
        # containers_list = lumeod.get_lumeo_containers()

        # if not containers_list:
        #     if os.getenv('NO_PROVISION', False):
        #         # pull the latest version of lumeo image, but not attempt to install it
        #         lumeod.download_container()
        #         sys.exit(0)
        #     else:
        #         # start a new container installation if no containers are found
        #         lumeod.install_container()

        print_menu()

        # if Lumeo containers are found, we list them
        lumeod.list_containers()

        while True:
            try:
                user_option = display.prompt_input("Enter the command")
                if user_option in COMMANDS:
                    COMMANDS[user_option][1]()
                else:
                    print("Error: Command is not recognized! Please select a valid command\n")
                    print_menu()
            except KeyboardInterrupt:
                sys.exit(0)
    else:
        # Perform a single operation and exit
        if args.container_name and args.command in ["stop", "restart", "remove", "logs", "shell", "wgm",
                                                    "write_hardware_information"]:
            COMMANDS[args.command][1](args.container_name)
        elif args.force_update and args.command == "update":
            COMMANDS[args.command][1](args.force_update)
        else:
            COMMANDS[args.command][1]()
            
            
if __name__ == "__main__":
    main()