#!/usr/bin/env python3
import os
import sys
import petname
import toml
import docker
import json

import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.nvidia as nvidia
import lumeo.scripts.gateway.docker as dockerutils
import lumeo.scripts.gateway.common as common
import lumeo.scripts.gateway.updater as updater
import lumeo.scripts.gateway.schedule as schedule

# Container versions:
# 1. Initial version
# 2. `--gpus all` on x86_64` vs `--runtime nvidia` on `aarch64`
# 3. '--privileged' mode is now required
LUMEO_CONTAINER_VERSION = "3"

# Get the information of current OS platform
os_platform_info = os.uname().machine

def get_lumeod_image():
    image = os.getenv("LUMEO_IMAGE")
    if not image:
        if os_platform_info == "aarch64":
            l4t_ver = nvidia.l4t_version()
            if l4t_ver and l4t_ver < "36":
                return "lumeo/gateway-nvidia-jetson"
            elif l4t_ver and l4t_ver >= "36":
                return "lumeo/gateway-nvidia-jetson-jetpack6"
            else:
                sys.exit("Error: Could not determine the Jetpack L4T version")
        elif os_platform_info == "x86_64":
            return "lumeo/gateway-nvidia-dgpu"
        else:
            sys.exit("Unsupported platform")
    return image


def list_containers(status="all"):
    if status == "running":
        show_all = False
    else:
        show_all = True

    containers_list = get_lumeo_containers(show_all=show_all)

    containers_names = []
    container_full_info = []
    for (idx, container) in enumerate(containers_list):
        containers_names.append(container.name)
        container_full_info.append(
            [
                str(idx + 1),
                container.name,
                container.status,
                container.attrs["Config"]["Labels"]["lumeo.gateway_id"],
                container.attrs["Config"]["Labels"]["lumeo.application_id"],
                container.labels["lumeo.container_version"],
                ",".join(container.image.tags)
            ]
        )

    headers = ["Index", "Name", "Status", "Gateway ID", "Application ID", "Version", "Image"]
    display.output_data(headers=headers, rows=container_full_info, title="\nList of Lumeo gateway containers installed:")
    return containers_names


def choose_container_with_prompt(status, action_description):
    containers_list = list_containers(status)
    if not containers_list:
        return None

    index_or_container_name = display.prompt_input(f"Insert the index or the name of the container to {action_description}:")

    try:
        index = int(index_or_container_name)
        if 1 <= index <= len(containers_list):
            return containers_list[index - 1]
        else:
            print("Invalid index")
            return None
    except ValueError:
        # If we couldn't parse input as a number, use the original string as a container name.
        container_name = index_or_container_name
        if container_name in containers_list:
            return container_name
        else:
            print("Container not found")
            return None


def device_requests():
    if os_platform_info == "aarch64":
        if nvidia.l4t_version() < "35.1":
            # "--gpus all" was required before JetPack 5.0.
            return [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
        else:
            return None
    elif os_platform_info == "x86_64":
        return [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
    else:
        raise RuntimeError("Unsupported platform: {}".format(os_platform_info))


def get_volume_bindings(container_name):
    volume_bindings = []
    existing_media_volume_mapping = None
    
    # If this is existing container, we need to check if there is a media volume already mapped
    if dockerutils.check_container_exists(container_name):
        # Check if there is a media volume already mapped
        container = dockerutils.DOCKER_CLIENT.containers.get(container_name)
        for mount in container.attrs['Mounts']:
            if mount['Destination'] != '/var/lib/lumeo/media':
                volume_bindings.append(f"{container_name}:{mount['Destination']}")
            else:
                existing_media_volume_mapping = f"{mount['Source']}:{mount['Destination']}"
    else:
        volume_bindings.append(f"{container_name}:/var/lib/lumeo")

    # Update media volume if LUMEO_MEDIA_VOLUME_PATH is set
    additional_media_volume_path = os.getenv("LUMEO_MEDIA_VOLUME_PATH")
    if not additional_media_volume_path:
        use_host_folder = display.prompt_input(f"Container {container_name}: Do you want to use or change host folder to store media saved locally in the container? (y/n)", default="n")
        if use_host_folder == "y":
            additional_media_volume_path = display.prompt_input(f"Container {container_name}: Provide absolute path to the media folder on the host (will be created if not exists) or 'remove' to remove an existing mapping:")
        
    if additional_media_volume_path:
        additional_media_volume_path = additional_media_volume_path.strip().lower()
        
        if additional_media_volume_path == 'remove':
            display.output_message(f"Container {container_name}: Removing media volume mapping for /var/lib/lumeo/media.", "info")
        else:
            # Check if the path is absolute
            if not os.path.isabs(additional_media_volume_path):
                display.output_message(f"Container {container_name}: Error: You must provide an absolute path for media volume. Currently specified: {additional_media_volume_path}", "error")
                return None

            # Check if the folder exists or try to create it
            display.output_message(f"Container {container_name}: Checking if media volume directory exists or trying to create it: {additional_media_volume_path}", "info")
            if not hostutils.ensure_directory_with_permissions(additional_media_volume_path):
                return None  # Exit if the directory setup failed

            # Append the volume to the list of volume bindings
            volume_bindings.append(f"{additional_media_volume_path}:/var/lib/lumeo/media")
            display.output_message(f"Container {container_name}: Media volume {additional_media_volume_path} mapping added for /var/lib/lumeo/media.", "info")
    elif existing_media_volume_mapping:
        volume_bindings.append(existing_media_volume_mapping)
        display.output_message(f"Container {container_name}: Media volume {existing_media_volume_mapping} mapping retained for /var/lib/lumeo/media.", "debug")
    else:
        display.output_message(f"Container {container_name}: No media volume mapping for /var/lib/lumeo/media found or configured.", "debug")

    return volume_bindings

def get_lumeo_containers(show_all=True, version=None):
    labels = []
    if version:
        labels.append("lumeo.container_version={}".format(version))

    containers_list = dockerutils.DOCKER_CLIENT.containers.list(
        all=show_all,
        filters={"label": labels},
    )

    return [container for container in containers_list 
            if "lumeo.gateway_id" in container.attrs["Config"]["Labels"]]


def download_container():
    # The only thing we do for OEM installs is to pull the latest
    # version of lumeo image. The rest will be done when the user
    # links a container to their account.
    image_name = get_lumeod_image()
    dockerutils.docker_download_image(image_name)
    return

def install_container():
    
    display.output_message("Installing Lumeo container...", "info")
        
    no_prompt = os.getenv("NO_PROMPT")
    lumeo_app_id = os.getenv("LUMEO_APP_ID")
    lumeo_api_key = os.getenv("LUMEO_API_KEY")
    lumeo_gateway_name = os.getenv("LUMEO_GATEWAY_NAME")
    lumeo_environment = os.getenv("LUMEO_ENVIRONMENT")
    lumeo_container_name_prefix = "lumeo-container-"
    auto_provision = lumeo_app_id and lumeo_api_key
    
    if no_prompt and not auto_provision:
        display.output_message("Error: `--no-prompt` requires `--app-id` and `--api-key`", "error")
        return
    
    common.install_common_dependencies()
    
    updater.install_update_gateway_updater()
                    
    # Pull the latest version of lumeo image    
    lumeo_image = get_lumeod_image()
    dockerutils.docker_download_image(lumeo_image)

    container_name = lumeo_gateway_name.replace(" ", "-").replace(":", "") if lumeo_gateway_name else lumeo_container_name_prefix + petname.Generate()

    user_container_name = display.prompt_input(f"Insert container name (or just press Enter for use default '{container_name}'):", default=container_name)
    if user_container_name:
        container_name = user_container_name

    if not dockerutils.check_container_exists(container_name):
        
        container_volume_bindings = get_volume_bindings(container_name)
        if not container_volume_bindings:
            return
        
        container_env = []
        if lumeo_environment:
            container_env.append(f"--env LUMEO_ENVIRONMENT=\'{lumeo_environment}\'")
        if not auto_provision:
            display.print_text("[bold]Please login into your Lumeo account[/bold]")
            container_env.append(f"--env CONTAINER_MODEL=\'Container {lumeo_image}\'")
        else:
            display.output_message(f"Performing the provision of Lumeo container '{container_name}' using the provided LUMEO_APP_ID & LUMEO_API_KEY):", "info")
            container_env.append(f"--env CONTAINER_MODEL=\'Container {lumeo_image}\'")
            container_env.append(f"--env LUMEO_API_KEY=\'{lumeo_api_key}\'")
            container_env.append(f"--env LUMEO_APP_ID=\'{lumeo_app_id}\'")

        # Got to perform this with system call as docker-py does not support interactive container execution
        if auto_provision:
            docker_cmd = "docker run -v {container}:/var/lib/lumeo --name {container} {env_str} --hostname {container} {image} provision"
        else:
            docker_cmd = "docker run -v {container}:/var/lib/lumeo -it --name {container} {env_str} --hostname {container} {image} provision"
        docker_cmd = docker_cmd.format(container=container_name, env_str=" ".join(container_env), image=lumeo_image)

        if hostutils.run_command(docker_cmd, sudo=True, useOsRun=True) == 0:
            dockerutils.DOCKER_CLIENT.api.remove_container(container_name, force=True)

            # At this point the volume has already been created, so we can write hardware info to it.
            write_hardware_information_to_container(container_name)

            # Read provision info from volume
            volume = dockerutils.DOCKER_CLIENT.volumes.get(container_name)
            mountpoint = volume.attrs.get("Mountpoint")

            toml_file = open(os.path.join(mountpoint, "lumeod.toml"), "r")
            lumeod_config = toml.load(toml_file)

            container_labels = {
                "com.centurylinklabs.watchtower.enable": "true",
                "lumeo.container_version": LUMEO_CONTAINER_VERSION,
                "lumeo.container_type": get_lumeod_image(),
                "lumeo.organization_id": lumeod_config["organization_id"],
                "lumeo.application_id": lumeod_config["application_id"],
                "lumeo.gateway_id": lumeod_config["gateway_id"],
            }

            # Temporary workaround until we pass the port mapping to provision
            if not dockerutils.DOCKER_CLIENT.containers.list(all=True,
                                                 filters={"label": "lumeo.primary_container"}
                                                 ):
                container_labels["lumeo.primary_container"] = "true"
                network_mode = "host"
                port_mapping = None
            else:
                network_mode = None
                port_mapping = {"8060/tcp": None}

            display.output_message("Starting container...", "info")
            
            jetson_model_name = nvidia.get_jetson_model_name()
            environment = {"JETSON_MODEL_NAME": jetson_model_name} if jetson_model_name else None

            if dockerutils.DOCKER_CLIENT.containers.run(
                    lumeo_image,
                    volumes=container_volume_bindings,
                    restart_policy={"MaximumRetryCount": 0, "Name": "always"},
                    name=container_name,
                    hostname=container_name,
                    network_mode=network_mode,
                    ports=port_mapping,
                    devices=nvidia.get_devices_for_container(),
                    device_requests=device_requests(),
                    runtime=nvidia.get_nvidia_docker_runtime(),
                    labels=container_labels,
                    detach=True,
                    environment=environment,
                    privileged=True,
                    ulimits=[docker.types.Ulimit(name="core", soft=0, hard=0)],
                    # Directly set ulimits to disable core dumps
            ):
                display.output_message("Container started!", "success")
        else:
            dockerutils.DOCKER_CLIENT.api.remove_container(container_name, force=True)
            display.output_message("Error: Provision on Lumeo failed", "error")
    else:
        display.output_message("Error: A container with name '{}' already exists".format(container_name), "error")
        
    return


def stop_container(container_name=None):
    container_name = container_name or choose_container_with_prompt("running", "stop")
    if container_name:
        try:    
            dockerutils.DOCKER_CLIENT.api.kill(container_name)
            display.output_message("Container stopped!", "success")
        except Exception as err:
            display.output_message(f"Error stopping container {container_name}: {err}", "error")


def upgrade_and_restart_container(container_name=None):
    if os_platform_info == "aarch64" and nvidia.l4t_version() < "35.1":
        display.output_message(
            "Couldn't restart the container because JetPack is outdated. Please, update JetPack or contact Lumeo support.",
            "error")
        return
    
    # Setup Jetson GPIO if needed
    jetson_model_name = nvidia.get_jetson_model_name()
    if jetson_model_name:
        nvidia.setup_jetson_gpio()

    if container_name is None:
        # If no explicit `container_name` is given, prompt the user.
        container_name = choose_container_with_prompt("all", "restart")
        if container_name is None:
            return

    current_container = dockerutils.DOCKER_CLIENT.containers.get(container_name)
    if not current_container:
        display.output_message("Container not found", "error")
        return

    container_volume_bindings = get_volume_bindings(container_name)
    if not container_volume_bindings:
        return

    # Get the image used by the current container
    current_image = current_container.attrs["Config"]["Image"]

    # Check if the current image has a specific tag like ':staging' or ':development'
    if ':' in current_image:
        image_base, current_tag = current_image.split(':')
    else:
        image_base = current_image
        current_tag = None

    # Preserve the tag if it's a special one, otherwise use get_lumeod_image
    if current_tag in ['staging', 'development']:
        final_image = f"{image_base}:{current_tag}"
    else:
        final_image = get_lumeod_image()  # Fallback to get_lumeod_image if no special tag is found

    # Pull the latest version of lumeo image
    #hostutils.run_command(f"docker pull {final_image}", sudo=True)
    dockerutils.docker_download_image(final_image)

    network_mode = current_container.attrs["HostConfig"]["NetworkMode"]
    port_mapping = current_container.attrs["HostConfig"]["PortBindings"]
    container_labels = current_container.attrs["Config"]["Labels"]

    container_labels["lumeo.container_version"] = LUMEO_CONTAINER_VERSION
    container_labels["lumeo.container_type"] = final_image

    environment = {"JETSON_MODEL_NAME": jetson_model_name} if jetson_model_name else None

    dockerutils.DOCKER_CLIENT.api.remove_container(container_name, force=True)

    # We restart an existing container, so the volume exists. Let's write fresh hardware info to it.
    write_hardware_information_to_container(container_name)

    if not dockerutils.DOCKER_CLIENT.containers.run(
            final_image,  # Use the preserved staging/development or fallback to default image tag
            volumes=container_volume_bindings,
            restart_policy={"MaximumRetryCount": 0, "Name": "always"},
            name=container_name,
            hostname=container_name,
            network_mode=network_mode,
            ports=port_mapping,
            devices=nvidia.get_devices_for_container(),
            device_requests=device_requests(),
            runtime=nvidia.get_nvidia_docker_runtime(),
            labels=container_labels,
            detach=True,
            environment=environment,
            privileged=True,
            ulimits=[docker.types.Ulimit(name="core", soft=0, hard=0)],  # Directly set ulimits to disable core dumps
    ):
        display.output_message(f"Failed to restart container {container_name}", "error")
        return

    display.output_message(f"Container {container_name} restarted with image {final_image}!", "success")    
    return


def upgrade_v2_containers():
    # Restart would change container version from v2 to v3.
    # Restart affects
    # - `x86` v2 containers with up-to-date NVIDIA driver
    # - Jetson v2 containers with up-to-date Jetpack
    if os_platform_info == "aarch64" and nvidia.l4t_version() < "35.1":
        display.output_message("Skipping v1/v2 containers upgrade because JetPack is outdated", "error")
        return False

    v2_containers = get_lumeo_containers(version=2)

    # Skip further checks if there are no v2 containers anyway.
    if not v2_containers:
        display.output_message("No outdated containers found.", "info")
        return True

    try:
        if os_platform_info == "x86_64" and nvidia.get_dgpu_driver_version() < 515:
            display.output_message("Skipping v2 containers restart because NVIDIA dGPU driver is outdated", "error")
            return False
    except:
        display.output_message(
            "[lumeo-container-update] Can't check dGPU driver version. Please make sure GPU drivers and nvidia-smi are installed",
            "error")
        return False

    for container in v2_containers:
        upgrade_and_restart_container(container.name)

    return True


def remove_container(container_name=None):
    container_name = container_name or choose_container_with_prompt("all", "remove")
    if container_name:
        try:
            dockerutils.DOCKER_CLIENT.api.remove_container(container_name, force=True)
            dockerutils.DOCKER_CLIENT.api.remove_volume(container_name, force=True)
            display.output_message("Container removed!", "success")
        except Exception as err:
            display.output_message(f"Error removing container {container_name}: {err}", "error")


def update_containers(force_update=False):

    common.update_common_dependencies()    
    
    remove_deprovisioned_containers()

    # TODO: Stop writing hardware information every hour when all lumeod's are updated to a release newer than 1.23.x.
    write_hardware_information_for_all_containers()

    if upgrade_v2_containers() and (force_update or schedule.check_update_schedule()):
        dockerutils.watchtower_trigger_update()

    updater.install_update_gateway_updater()
    
    return


def remove_deprovisioned_containers():
    containers_list = get_lumeo_containers()

    for container in containers_list:
        try:
            if container.name != "lumeo-watchtower":
                # Read provision info from volume
                volume = dockerutils.DOCKER_CLIENT.volumes.get(container.name)
                mountpoint = volume.attrs.get("Mountpoint")

                if os.path.isfile(os.path.join(mountpoint, "lumeod.toml")):
                    toml_file = open(os.path.join(mountpoint, "lumeod.toml"), "r")
                    lumeod_config = toml.load(toml_file)

                    # Check if there's some container with deprovisioned=true label on lumeod.toml
                    if "deprovisioned" in lumeod_config:
                        if lumeod_config["deprovisioned"] is True:
                            # In that case, remove the container image & volume
                            print("[lumeo-container-update] Deprovision detected, removing the following "
                                  "Lumeo container and volume: {}".format(container.name))
                            dockerutils.DOCKER_CLIENT.api.remove_container(container.name, force=True)
                            dockerutils.DOCKER_CLIENT.api.remove_volume(container.name, force=True)
        except Exception as err:
            display.output_message("[lumeo-container-update] Exception: {}".format(err), "error")


def logs(container_name=None):
    container_name = container_name or choose_container_with_prompt("all", "print logs")
    if container_name:
        display.print_text(dockerutils.DOCKER_CLIENT.api.logs(container_name).decode("ascii"))


def shell(container_name=None):
    container_name = container_name or choose_container_with_prompt("running", "access with interactive shell")
    if container_name:
        hostutils.run_command(f"docker exec -it {container_name} bash", useOsRun=True)

def write_hardware_information_for_all_containers():
    containers_list = get_lumeo_containers()
    for container in containers_list:
        write_hardware_information_to_container(container.name)


# Write output from various hardware information tools to container volume.
# Lumeod would then parse gateway specifications from these files.

def write_hardware_information_to_container(container_name):
    try:
        display.output_message(f"Getting data directory for container {container_name}", "debug")
        volume = dockerutils.DOCKER_CLIENT.volumes.get(container_name)
        mount_point = volume.attrs['Mountpoint']
        hardware_information_dir = f"{mount_point}/hardware_information"

        display.output_message(f"Attempting to remove directory: {hardware_information_dir}", "debug")
        hostutils.run_command(f"rm -rf {hardware_information_dir}", sudo=True)
        display.output_message(f"Removed directory: {hardware_information_dir}", "debug")

        display.output_message(f"Writing hardware information to {hardware_information_dir} ...", "debug")
        write_hardware_information_to_directory(hardware_information_dir)

        display.output_message("Changing owner ...", "debug")
        lumeod_file = f"{mount_point}/lumeod.toml"
        stat_info = os.stat(lumeod_file)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        hostutils.run_command(f"chown -R {uid}:{gid} {hardware_information_dir}", sudo=True)

        display.output_message("Hardware information written.", "info")
    except IndexError:
        display.output_message("Error: The container does not have any volumes.", "error")
    except KeyError:
        display.output_message("Error: The volume does not have a source.", "error")
    except FileNotFoundError:
        display.output_message(f"Error: File not found: {lumeod_file}", "error")
    except Exception as error:
        display.output_message(f"Exception: {error}", "error")


def write_hardware_information_to_directory(directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the commands and their corresponding output files
    commands = [
        ('lshw -json', 'lshw.json'),
        ('lscpu --json', 'lscpu.json'),
        ('nvpmodel --verbose --parse', 'nvpmodel-all.txt'),
        ('nvpmodel --query', 'nvpmodel-current.txt')
    ]

    for command, file in commands:
        result = hostutils.run_command(command, silent=True)
        if result is None:
            continue

        # Write the output to the corresponding file
        with open(os.path.join(directory, file), 'w') as f:
            f.write(result)

    # Save disk info
    command = 'smartctl --json --scan'
    result = hostutils.run_command(command)
    if result is None:
        return

    disk_info = []
    scanned_disks = json.loads(result).get('devices', [])
    for disk in scanned_disks:
        disk_name = disk.get('name', '')
        command = f'smartctl --json --info {disk_name}'
        result = hostutils.run_command(command)
        if result is not None:
            disk_info.append(json.loads(result))

    # Write the output to the corresponding file
    with open(os.path.join(directory, 'smartctl.json'), 'w') as f:
        json.dump(disk_info, f, indent=4)  # Prettify JSON output
