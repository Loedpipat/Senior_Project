# Mininet & Mininet-WiFi Setup Guide

## Basic Information
- **IP**: `192.168.56.101/24`
- **Version**: `2.3.0`
- **How to install ref**: [Ref. 1](https://brianlinkletter.com/2016/02/using-the-opendaylight-sdn-controller-with-the-mininet-network-emulator/)
[Ref. 2](https://brianlinkletter.com/2013/09/set-up-mininet/)
- **Installation Guide**: [How to install mininet](https://mininet.org/download/)
- **Username**: `mininet`
- **Password**: `0934239213`

---

## 0. Download a Mininet VM Image
**Download a Mininet VM Image from**: [Mininet Releases.](https://github.com/mininet/mininet/releases/)
- Then put image on your hyperviser eg. VirtualBox

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
              addresses: [192.168.56.101/24]
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
## 2. Mininet-Wifi Installation
**Book**: [Mininet-Wifi Book](*mininet-wifi-ebook-preview-EN-20191212.pdf)
- Git clone installation:
    ```bash
    $ sudo apt-get install git
    $ git clone https://github.com/intrig-unicamp/mininet-wifi
    $ cd mininet-wifi
    $ sudo util/install.sh -Wlnfv 
    ```
## 3. Get Started
- Run the topology file:
    ```bash
    $ cd mininet-wifi
    $ sudo mn –wifi
    ```
    - If use script
    ```bash
    $ cd mininet-wifi
    $ sudo python3 lille_star_topology.py
    ```
- OpenFlow Table Command:
    ```bash
    mininet-wifi $ h1 ifconfig
    mininet-wifi $ sta1 iwconfig
    mininet-wifi $ 
    ```
## 4. Install Extension Tools
- More tools if needed:
    ```bash
    $ sudo apt install iperf3
    $ sudo apt install wireshark
    $ sudo apt install htop 
    ```
## Extra Command
- Change Username :
    ```bash
    $ sudo usermod -l newuser olduser
    $ sudo mv /home/olduser /home/newuser
    $ sudo usermod -d /home/newuser -m newuser
    ```
- Change Password :
    ```bash
    $ passwd
    ```
    - Put your current password
    ```bash
    $ Current password:
    ```
    - Put your new password
    ```bash
    $ New password:
    ```
    - Put your new password again
    ```bash
    $ Retype new password:
    ```
    ```bash
    $ passwd: password updated successful
    ``` 
- Delete File :
    ```bash
    $ sudo rm -i file_name
    ```
- Create Folder :
    ```bash
    $ sudo mkdir senior_project folder_name
    ```
- Create File :
    ```bash
    $ sudo touch file_name
    ```
- Create and access File :
    ```bash
    $ sudo nano file_name
    ```
- See File :
    ```bash
    $ sudo cat file_name
    ```
- Clear File :
    ```bash
    $ sudo truncate -s 0 file_name
    ``` 