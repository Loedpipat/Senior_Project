# Containernet Setup Guide

## Basic Information
- **IP**: `192.168.56.150/24`
- **Version**: `3.0`
- **Installation Guide**: [Containernet GitHub](https://github.com/ramonfontes/containernet)
- **Username**: `containernet`
- **Password**: `0934239213`

---

## 0. Add Containernet User to Sudo Group
- Entering to root for set user:
    ```bash
    $ su -
    # usermod -aG sudo containernet
    # groups containernet
    ```
- Logout and re-login to apply changes:
## 1. Prepare the Operating System
- Set up tools and systems:
    ```bash
    $ sudo apt install net-tools
    $ sudo apt-get -y update
    $ sudo apt-get -y upgrade
    $ sudo apt install openssh-server
    $ sudo service ssh status
    ```
- Configure Network:
    ```bash
    $ sudo nano /etc/netplan/01-netcfg.yaml
    ```
- Insert the following configuration .yaml:
    ```bash
    network:
      version: 2
      renderer: networkd
      ethernets:
          enp0s8:
              dhcp4: no
              addresses: [192.168.56.150/24]
              gateway4: 192.168.56.1
              nameservers:
                addresses: [8.8.8.8, 8.8.4.4]
    ```
- Apply the changes and reboot:
    ```bash
    $ sudo netplan apply
    $ ip addr show enp0s8
    $ sudo reboot
    ```
## 2. Containernet Installation
- Bare-metal installation:
    ```bash
    $ sudo apt install git
    $ git clone https://github.com/ramonfontes/containernet.git
    $ cd containernet
    $ sudo util/install.sh -W
    ```
- Created Folder:
    ```bash
    $ cd containernet
    $ sudo mkdir senior_project
    $ nano topology.py
    ```
## 3. Get Started
- Run the topology file:
    ```bash
    $ cd containernet
    $ sudo python senior_project/topology.py
    ```
## 4. Install Extension Tools
- More tools if needed:
    ```bash
    $ sudo apt install iperf3
    $ sudo apt install wireshark
    $ sudo apt install htop 
    ```
## Extra Command
- Check Existing Containers:
    ```bash
    $ sudo docker ps -a
    ```
- Remove the Existing Container:
    ```bash
    $ sudo docker rm -f mn.sta1
    ```
- Restart Docker:
    ```bash
    $ sudo systemctl restart docker
    ```
- *Stop all running containers (if any):
    ```bash
    $ sudo docker stop $(sudo docker ps -aq)
    ```
- *Remove all containers:
    ```bash
    $ sudo docker rm $(sudo docker ps -aq)
    ```
- *Use Linux without GUI:
    ```bash
    $ sudo systemctl set-default multi-user.target
    $ sudo reboot
    ```
- *Use Linux with GUI:
    ```bash
    $ sudo systemctl set-default graphical.target
    $ sudo reboot
    ```
## Note!!
    ```bash
    containernet> sta1 lsb_releas -a
    containernet> sta1 df
    containernet> sta1 iw dev
    containernet> sta1 iw dev sta1-wlan0 scan
    containernet> sta1 iw dev sta1-wlan0 connect new-ssid
    containernet> sta1 iw dev sta1-wlan0 info
    containernet> sta1 iw dev sta1-wlan0 link
    ```