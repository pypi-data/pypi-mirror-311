import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.nvidia as nvidia
import lumeo.scripts.gateway.docker as dockerutils

def install_common_dependencies():
    
    display.output_message("Installing common dependencies...", status='info')
        
    hostutils.check_os()
    
    hostutils.check_disk_space()
    
    # Install host dependencies
    hostutils.setup_host_common()
    
    # Setup Nvidia DGPU drivers
    nvidia.check_nvidia_dgpu_driver()
    
    nvidia.check_disable_nvidia_driver_updates()
    
    # Setup Jetson specific components
    nvidia.enable_jetson_clocks()
    
    jetson_model_name = nvidia.get_jetson_model_name()
    if jetson_model_name:
        nvidia.setup_jetson_gpio()    
    nvidia.install_jetson_extras()
    
    # Setup Docker and NVIDIA toolkit
    dockerutils.install_docker_and_nvidia_toolkit()
    
    dockerutils.check_set_docker_data_dir()
    
    dockerutils.set_docker_logs_configuration()
    
    dockerutils.fix_nvidia_nvml_init_issue()
    
    # Disable X server
    hostutils.prompt_disable_x_server()
    
    # Start watchtower
    dockerutils.start_watchtower()
    
    return

    
def update_common_dependencies():
    
    dockerutils.fix_nvidia_nvml_init_issue()
    
    nvidia.enable_jetson_clocks()

    dockerutils.set_docker_logs_configuration()
    
    dockerutils.migrate_watchtower()
    
    return
    