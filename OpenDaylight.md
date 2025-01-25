# OpenDaylight Setup Guide

## Basic Information
These are configured when the user installs the virtual machine.
- **IP**: `192.168.56.201/24`
- **Version**: `0.84`
- **Installation Guide**: [How to install (1)](https://brianlinkletter.com/2016/02/using-the-opendaylight-sdn-controller-with-the-mininet-network-emulator/ )
[How to install (2)](https://brianlinkletter.com/2016/02/using-the-opendaylight-sdn-controller-with-the-mininet-network-emulator/ )
- **Username**: `opendaylight`
- **Password**: `0934239213`

---

## 0. Add Opendaylight User to Sudo Group
- Entering to root for set user:
    ```bash
    $ su -
    # usermod -aG sudo opendaylight
    # groups opendaylight
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
              addresses: [192.168.56.201/24]
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
## 2. Java Setup
- Install the Java JRE:
    ```bash
    $ sudo apt-get -y install openjdk-8-jre
    $ sudo update-alternatives --config java
    ```
- Verify the Java installation path:
    ```bash
    $ ls -l /etc/alternatives/java
    ```
- Set JAVA_HOME in your environment:
    ```bash
    $ echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> ~/.bashrc
    $ source ~/.bashrc
    $ echo $JAVA_HOME
    ```
## 3. OpenDaylight Installation
- Download from webpage:
    ```bash
    $ wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
    ```
- Install OpenDaylight:
    ```bash
    $ unzip karaf-0.8.4.zip
    ```
- Navigate to the OpenDaylight directory:
    ```bash
    $ cd karaf-0.8.4/
    ```
- Start the OpenDaylight Karaf shell:
    ```bash
    $ ./bin/karaf
    ```
- Install the necessary features:
    ```bash
    feature:install odl-restconf-all odl-l2switch-all odl-mdsal-apidocs odl-dlux-core
    feature:install odl-dluxapps-nodes odl-dluxapps-yangui odl-dluxapps-yangman odl-dluxapps-topology odl-dluxapps-yangutils odl-dluxapps-applications odl-dluxapps-yangvisualizer
    ```
- Exit the OpenDaylight shell:
    ```bash
    <ctrl-d>
    ```
## 4. Get Started
- Restart OpenDaylight:
    ```bash
    $ cd karaf-0.8.4/
    $ ./bin/karaf
    ```
- Access the web interface at: http://192.168.56.201:8181/index.html