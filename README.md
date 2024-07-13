## Automated VM Creation and Configuration




This Python script automates the creation, configuration, and management of Virtual Machines (VMs) using VirtualBox, SSH (Paramiko), and Netplan. It allows for:

Importing VMs from a base OVA file.
Setting hostnames inside VMs.
Configuring IP addresses using Netplan.
Rebooting VMs after IP configuration.
Features:
Dynamic Configuration: Set hostname and IP addresses programmatically.
Logging: Detailed logging of each step (INFO, ERROR) to vm_creation.log.
User Interaction: Prompts for the starting series of IP addresses.
Requirements:
Python 3.x
Paramiko (pip install paramiko)
VirtualBox with VMs based on an OVA file
Usage:
Modify script variables (base_ova_file, num_vms, etc.) as needed.
Run the script and follow prompts for IP series.
Feel free to contribute and enhance this script for your virtualization needs!

# Steps for Configurtion

### Basevm must be host adopter network with static ip
#### ~ using this only it set baseip

### u need to install ssh in ur base vm
#### ~ install ssh server in base ip 

### check /etc/netplan ~ls to check what file name for network manager
#### ~ check the /etc/netplan/ inside file name of network manger note file name and update the in script

### create a basevm and export as ova file
#### ~ ensure the base ip using cmd { ifconfig } and note it down

### change your base_ip accoding to ur ip
#### ~ change in script update ur base ip in script

### configure the script according to ur need
#### ~ change the number series for ur wish default it set to { 10 } 

@Any doubts ping me!
