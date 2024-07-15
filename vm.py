# import subprocess
# import time
# import paramiko
# import os
# import logging

# # Define variables
# base_ova_file = 'Basevm.ova'  # Path to the base OVA file
# base_vm_ip = '192.168.56.2'  # Updated IP address of the base VM
# subnet = '24'  # Subnet mask (e.g., 24 for /24 subnet)
# gateway = '192.168.56.1'  # Gateway IP address
# ssh_user = 'user01'  # SSH username
# ssh_password = 'admin@123'  # SSH password
# prefix = 'my_vm'  # Prefix for VM names
# num_vms = 3  # Number of VMs to create

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='vm_creation.log', filemode='w')
# logger = logging.getLogger(__name__)

# # Function to import and start VM
# def import_and_start_vm(base_ova_file, vm_name):
#     logger.info(f'Importing VM {vm_name} from {base_ova_file}')
#     subprocess.run(['VBoxManage', 'import', base_ova_file, '--vsys', '0', '--vmname', vm_name])
#     logger.info(f'Starting VM {vm_name}')
#     subprocess.run(['VBoxManage', 'startvm', vm_name, '--type', 'headless'])
#     logger.info(f'Waiting for VM {vm_name} to start')
#     time.sleep(120)  # Increase wait time for VM startup

# # Function to configure hostname inside the VM using paramiko
# def configure_hostname(base_vm_ip, hostname):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     logger.info(f'Configuring hostname {hostname} for VM with IP {base_vm_ip}')
    
#     # Attempt to connect multiple times with a delay to ensure VM is ready
#     connected = False
#     for _ in range(10):
#         try:
#             client.connect(base_vm_ip, username=ssh_user, password=ssh_password)
#             connected = True
#             break
#         except Exception as e:
#             logger.warning(f'SSH connection failed: {e}')
#             time.sleep(30)  # Wait before retrying

#     if not connected:
#         logger.error("Failed to connect to VM via SSH after multiple attempts")
#         raise Exception("Failed to connect to VM via SSH after multiple attempts")
    
#     # Set the hostname inside the VM
#     logger.info(f'Setting hostname {hostname} on VM')
#     stdin, stdout, stderr = client.exec_command(f'sudo hostnamectl set-hostname {hostname}')
#     logger.info(stdout.read().decode())
#     logger.error(stderr.read().decode())
    
#     client.close()

# # Function to configure IP address using Netplan inside the VM
# def configure_ip_address(base_vm_ip, subnet, series, vm_name):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     logger.info(f'Configuring IP address for {vm_name}')
    
#     # Calculate IP address
#     ip_address = f'192.168.56.{series}/{subnet}'
    
#     # Attempt to connect multiple times with a delay to ensure VM is ready
#     connected = False
#     for _ in range(10):
#         try:
#             client.connect(base_vm_ip, username=ssh_user, password=ssh_password)
#             connected = True
#             break
#         except Exception as e:
#             logger.warning(f'SSH connection failed: {e}')
#             time.sleep(30)  # Wait before retrying

#     if not connected:
#         logger.error("Failed to connect to VM via SSH after multiple attempts")
#         raise Exception("Failed to connect to VM via SSH after multiple attempts")
    
#     # Create and upload Netplan configuration using nano editor
#     logger.info(f'Creating and uploading Netplan configuration on {vm_name}')
#     netplan_config = f"""
#     network:
#       version: 2
#       renderer: networkd
#       ethernets:
#         enp0s3:
#           dhcp4: no
#           addresses:
#             - {ip_address}
#           gateway4: {gateway}
#           nameservers:
#             addresses:
#               - 8.8.8.8
#               - 8.8.4.4
#     """
#     # Write configuration to a temporary file on the remote VM using nano
#     nano_command = f'echo "{netplan_config}" | sudo tee /etc/netplan/01-network-manager-all.yaml'
#     stdin, stdout, stderr = client.exec_command(nano_command)
#     logger.info(stdout.read().decode())
#     logger.error(stderr.read().decode())
    
#     # Apply Netplan configuration
#     logger.info(f'Applying Netplan configuration on {vm_name}')
#     stdin, stdout, stderr = client.exec_command('sudo netplan apply')
#     client.close()

# # Main function to create and configure VMs
# def create_and_configure_vms(base_ova_file, num_vms, base_vm_ip, subnet, gateway, prefix):
#     for i in range(1, num_vms + 1):
#         vm_name = f'{prefix}_{i}'
#         hostname = f'{prefix}_{i}'  # Ensure hostname is same as VM name
#         import_and_start_vm(base_ova_file, vm_name)
        
#         # Check if the VM is up and running before attempting to configure it
#         if os.system(f"ping -c 1 {base_vm_ip}") == 0:  # For Windows use 'ping -n 1', for Unix use 'ping -c 1'
#             configure_hostname(base_vm_ip, hostname)
#             configure_ip_address(base_vm_ip, subnet, 10 + i, vm_name)  # Adjust series start as needed
#             logger.info(f'Started and configured hostname and IP address for VM {vm_name} with hostname {hostname}')
#         else:
#             logger.error(f'Failed to reach VM {vm_name} at IP {base_vm_ip}')

# # Call the main function to create and configure VMs
# create_and_configure_vms(base_ova_file, num_vms, base_vm_ip, subnet, gateway, prefix)
import subprocess
import time
import paramiko
import os
import logging

# Define variables
base_ova_file = 'Basevm.ova'  # Path to the base OVA file
base_vm_ip = '192.168.56.2'  # Updated IP address of the base VM
subnet = '24'  # Subnet mask (e.g., 24 for /24 subnet)
gateway = '192.168.56.1'  # Gateway IP address
ssh_user = 'user01'  # SSH username
ssh_password = 'admin@123'  # SSH password
prefix = 'my_vm'  # Prefix for VM names
num_vms = 3  # Number of VMs to create

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='vm_creation.log', filemode='w')
logger = logging.getLogger(__name__)

# Function to import and start VM
def import_and_start_vm(base_ova_file, vm_name):
    logger.info(f'Importing VM {vm_name} from {base_ova_file}')
    subprocess.run(['VBoxManage', 'import', base_ova_file, '--vsys', '0', '--vmname', vm_name])
    logger.info(f'Starting VM {vm_name}')
    subprocess.run(['VBoxManage', 'startvm', vm_name, '--type', 'headless'])
    logger.info(f'Waiting for VM {vm_name} to start')
    time.sleep(120)  # Increase wait time for VM startup

# Function to configure hostname inside the VM using paramiko
def configure_hostname(base_vm_ip, hostname):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.info(f'Configuring hostname {hostname} for VM with IP {base_vm_ip}')
    
    # Attempt to connect multiple times with a delay to ensure VM is ready
    connected = False
    for _ in range(10):
        try:
            client.connect(base_vm_ip, username=ssh_user, password=ssh_password)
            connected = True
            break
        except Exception as e:
            logger.warning(f'SSH connection failed: {e}')
            time.sleep(30)  # Wait before retrying

    if not connected:
        logger.error("Failed to connect to VM via SSH after multiple attempts")
        raise Exception("Failed to connect to VM via SSH after multiple attempts")
    
    # Set the hostname inside the VM
    logger.info(f'Setting hostname {hostname} on VM')
    stdin, stdout, stderr = client.exec_command(f'sudo hostnamectl set-hostname {hostname}')
    logger.info(stdout.read().decode())
    logger.error(stderr.read().decode())
    
    client.close()

# Function to configure IP address using Netplan inside the VM
def configure_ip_address(base_vm_ip, subnet, series, vm_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.info(f'Configuring IP address for {vm_name}')
    
    # Calculate IP address
    ip_address = f'192.168.56.{series}/{subnet}'
    
    # Attempt to connect multiple times with a delay to ensure VM is ready
    connected = False
    for _ in range(10):
        try:
            client.connect(base_vm_ip, username=ssh_user, password=ssh_password)
            connected = True
            break
        except Exception as e:
            logger.warning(f'SSH connection failed: {e}')
            time.sleep(30)  # Wait before retrying

    if not connected:
        logger.error("Failed to connect to VM via SSH after multiple attempts")
        raise Exception("Failed to connect to VM via SSH after multiple attempts")
    
    # Create and upload Netplan configuration using nano editor
    logger.info(f'Creating and uploading Netplan configuration on {vm_name}')
    netplan_config = f"""
    network:
      version: 2
      renderer: networkd
      ethernets:
        enp0s3:
          dhcp4: no
          addresses:
            - {ip_address}
          gateway4: {gateway}
          nameservers:
            addresses:
              - 8.8.8.8
              - 8.8.4.4
    """
    # Write configuration to a temporary file on the remote VM using nano
    nano_command = f'echo "{netplan_config}" | sudo tee /etc/netplan/01-network-manager-all.yaml'
    stdin, stdout, stderr = client.exec_command(nano_command)
    logger.info(stdout.read().decode())
    logger.error(stderr.read().decode())
    
    # Apply Netplan configuration
    logger.info(f'Applying Netplan configuration on {vm_name}')
    stdin, stdout, stderr = client.exec_command('sudo netplan apply')
    client.close()

# Main function to create and configure VMs
def create_and_configure_vms(base_ova_file, num_vms, base_vm_ip, subnet, gateway, prefix):
    hostnames = ['thala', 'vijay', 'dhanush']  # Predefined hostnames
    for i in range(1, num_vms + 1):
        vm_name = f'{prefix}_{i}'
        hostname = hostnames[i - 1]  # Select hostname from predefined list
        
        import_and_start_vm(base_ova_file, vm_name)
        
        # Check if the VM is up and running before attempting to configure it
        if os.system(f"ping -c 1 {base_vm_ip}") == 0:  # For Windows use 'ping -n 1', for Unix use 'ping -c 1'
            configure_hostname(base_vm_ip, hostname)
            configure_ip_address(base_vm_ip, subnet, 10 + i, vm_name)  # Adjust series start as needed
            logger.info(f'Started and configured hostname and IP address for VM {vm_name} with hostname {hostname}')
        else:
            logger.error(f'Failed to reach VM {vm_name} at IP {base_vm_ip}')

# Call the main function to create and configure VMs
create_and_configure_vms(base_ova_file, num_vms, base_vm_ip, subnet, gateway, prefix)
