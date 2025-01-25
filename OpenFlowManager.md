# OpenFlow Management (OFM) Installation Guide

## Basic Information
- **IP**: `192.168.56.61/24`
- **Version**: `0.8.4`
- **Installation Guide**: 
  - [Node.js Installation](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04)
  - [OpenFlow App GitHub](https://github.com/CiscoDevNet/OpenDaylight-Openflow-App)
- **Server Credentials**:
  - **Username**: `loedpipat`
  - **Password**: `0934239213`
- **ODL Credentials**:
  - **Username**: `admin`
  - **Password**: `admin`

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
              addresses: [192.168.56.61/24]
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
## 2. Install Node.js
- Download and set up the Node.js repository:
    ```bash
    $ cd ~
    $ curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh
    ```
- Review the setup script:
    ```bash
    $ nano /tmp/nodesource_setup.sh
    ```
- Run the setup script:
    ```bash
    $ sudo bash /tmp/nodesource_setup.sh
    ```
- Install Node.js:
    ```bash
    $ sudo apt install nodejs
    $ node -v
    ```
- Install essential tools:
    ```bash
    $ sudo apt-get install -y git
    $ sudo npm install -g grunt-cli
    $ sudo apt-get install build-essential
    ```
## 3. Install and Configure OpenFlow App
- Clone the OpenFlow App repository:
    ```bash
    $ git clone https://github.com/CiscoDevNet/OpenDaylight-Openflow-App.git
    ```
- Update the configuration to point to your OpenDaylight IP:
    ```bash
    $ sed -i 's/localhost/192.168.56.201/g' ./OpenDaylight-Openflow-App/ofm/src/common/config/env.module.js
    ```
- Install dependencies and start the application:
    ```bash
    $ cd OpenDaylight-Openflow-App/ && sudo npm install
    $ grunt
    ```
- Access the application:
    ```bash
    URL: http://192.168.56.61:9000
    ```
## 4. Get Started
- Restart OpenFlow Management:
    ```bash
    $ sed -i 's/localhost/192.168.56.201/g' ./OpenDaylight-Openflow-App/ofm/src/common/config/env.module.js
    $ cd OpenDaylight-Openflow-App/
    $ grunt
    ```
- Access the web interface at: http://192.168.56.61:9000  