#!/usr/bin/python
import time  # Import the time module to handle time-related tasks

from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, RemoteController

def topology():
    net = Containernet()

    info("*** Adding controller ODL: 192.168.56.201\n")
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.201', port=6633)

    info("*** Adding Access Points\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6')
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11')
    ap4 = net.addAccessPoint('ap4', ssid='ssid-ap4', mode='g', channel='1')
    ap5 = net.addAccessPoint('ap5', ssid='ssid-ap5', mode='g', channel='6')
    ap6 = net.addAccessPoint('ap6', ssid='ssid-ap6', mode='g', channel='11')
    ap7 = net.addAccessPoint('ap7', ssid='ssid-ap7', mode='g', channel='1')
    ap8 = net.addAccessPoint('ap8', ssid='ssid-ap8', mode='g', channel='6')
    ap9 = net.addAccessPoint('ap9', ssid='ssid-ap9', mode='g', channel='11')
    ap10 = net.addAccessPoint('ap10', ssid='ssid-ap10', mode='g', channel='1')

    info("*** Adding OpenFlow switches\n")
    switches = {f's{i}': net.addSwitch(f's{i}') for i in range(1, 11)}

    info('*** Adding Docker Stations (IoT Devices)\n')
    Ms = []
    Zs = []
    Ds = []
    WCAMs = []
    WLCAMs = []

    # IoT-LAB M3 Devices (m1 to m10)
    m_devices = [
        ('10.0.1.1', '00:02:00:00:01:01'), ('10.0.2.1', '00:02:00:00:02:01'),
        ('10.0.3.1', '00:02:00:00:03:01'), ('10.0.4.1', '00:02:00:00:04:01'),
        ('10.0.5.1', '00:02:00:00:05:01'), ('10.0.6.1', '00:02:00:00:06:01'),
        ('10.0.7.1', '00:02:00:00:07:01'), ('10.0.8.1', '00:02:00:00:08:01'),
        ('10.0.9.1', '00:02:00:00:09:01'), ('10.0.10.1', '00:02:00:00:0A:01')
    ]
    for i, (ip, mac) in enumerate(m_devices, 1):
        sta = net.addStation(f'm{i}', ip=ip, mac=mac, cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.1")
        Ms.append(sta)

    # Zolertia Firefly Devices (z1 to z10)
    z_devices = [
        ('10.0.1.2', '00:02:00:00:01:02'), ('10.0.2.2', '00:02:00:00:02:02'),
        ('10.0.3.2', '00:02:00:00:03:02'), ('10.0.4.2', '00:02:00:00:04:02'),
        ('10.0.5.2', '00:02:00:00:05:02'), ('10.0.6.2', '00:02:00:00:06:02'),
        ('10.0.7.2', '00:02:00:00:07:02'), ('10.0.8.2', '00:02:00:00:08:02'),
        ('10.0.9.2', '00:02:00:00:09:02'), ('10.0.10.2', '00:02:00:00:0A:02')
    ]
    for i, (ip, mac) in enumerate(z_devices, 1):
        sta = net.addStation(f'z{i}', ip=ip, mac=mac, cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.2")
        Zs.append(sta)

    # Decawave DWM1001 Devices (d1 to d10)
    d_devices = [
        ('10.0.1.3', '00:02:00:00:01:03'), ('10.0.2.3', '00:02:00:00:02:03'),
        ('10.0.3.3', '00:02:00:00:03:03'), ('10.0.4.3', '00:02:00:00:04:03'),
        ('10.0.5.3', '00:02:00:00:05:03'), ('10.0.6.3', '00:02:00:00:06:03'),
        ('10.0.7.3', '00:02:00:00:07:03'), ('10.0.8.3', '00:02:00:00:08:03'),
        ('10.0.9.3', '00:02:00:00:09:03'), ('10.0.10.3', '00:02:00:00:0A:03')
    ]
    for i, (ip, mac) in enumerate(d_devices, 1):
        sta = net.addStation(f'd{i}', ip=ip, mac=mac, cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.3")
        Ds.append(sta)

    # Add Wire and Wireless Cameras (WCAMs and WLCAMs)
    info("*** Adding Wire Cameras (High CPU Usage)\n")
    WCAMs = []
    wcam_devices = [
        ('10.0.1.4', '00:02:00:00:01:04'), ('10.0.2.4', '00:02:00:00:02:04'),
        ('10.0.3.4', '00:02:00:00:03:04'), ('10.0.4.4', '00:02:00:00:04:04'),
        ('10.0.5.4', '00:02:00:00:05:04'), ('10.0.6.4', '00:02:00:00:06:04'),
        ('10.0.7.4', '00:02:00:00:07:04'), ('10.0.8.4', '00:02:00:00:08:04'),
        ('10.0.9.4', '00:02:00:00:09:04'), ('10.0.10.4', '00:02:00:00:0A:04')
    ]
    for i, (ip, mac) in enumerate(wcam_devices, 1):
        sta = net.addDocker(f'wcam{i}', ip=ip, mac=mac, dimage="mininet-wifi-custom", cpus="0.5")
        WCAMs.append(sta)

    info("*** Adding Wireless Cameras (High CPU Usage)\n")
    WLCAMs = []
    wlcam_devices = [
        ('10.0.1.5', '00:02:00:00:01:05'), ('10.0.2.5', '00:02:00:00:02:05'),
        ('10.0.3.5', '00:02:00:00:03:05'), ('10.0.4.5', '00:02:00:00:04:05'),
        ('10.0.5.5', '00:02:00:00:05:05'), ('10.0.6.5', '00:02:00:00:06:05'),
        ('10.0.7.5', '00:02:00:00:07:05'), ('10.0.8.5', '00:02:00:00:08:05'),
        ('10.0.9.5', '00:02:00:00:09:05'), ('10.0.10.5', '00:02:00:00:0A:05')
    ]
    for i, (ip, mac) in enumerate(wlcam_devices, 1):
        sta = net.addStation(f'wlcam{i}', ip=ip, mac=mac, cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
        WLCAMs.append(sta)

    info("*** Adding host (Network Server)\n")
    server = net.addDocker('server', ip='10.0.0.200', dimage="mininet-wifi-custom", cpus="1")

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

    # Creating links for stations and cameras
    info('*** Creating links\n')
    net.addLink(ap1, switches['s1'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap2, switches['s1'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap3, switches['s2'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap4, switches['s2'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap5, switches['s3'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap6, switches['s3'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap7, switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap8, switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap9, switches['s5'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap10, switches['s5'], cls=TCLink, delay='50ms', bw=10)

    for i in range(10):  # Only 10 stations in each category
        ap = f'ap{i + 1}'  # Distribute stations evenly to APs
        net.addLink(WCAMs[i], eval(ap), cls=TCLink, delay='50ms', bw=5)

    # Core network connections (up to s10)
    net.addLink(switches['s1'], switches['s6'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s2'], switches['s6'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s3'], switches['s7'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s4'], switches['s7'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s5'], switches['s7'], cls=TCLink, delay='50ms', bw=10)

    net.addLink(switches['s6'], switches['s8'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s7'], switches['s9'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s8'], switches['s10'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s9'], switches['s10'], cls=TCLink, delay='50ms', bw=10)

    net.addLink(server, switches['s10'], cls=TCLink, delay='50ms', bw=10)

    # Start network and configure nodes
    info('*** Starting network\n')
    net.start()
    c0.start()

    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    ap4.start([c0])
    ap5.start([c0])
    ap6.start([c0])
    ap7.start([c0])
    ap8.start([c0])
    ap9.start([c0])
    ap10.start([c0])

    for s in switches.values():
        s.start([c0])

    # Ensuring WiFi connectivity
    info('*** Ensuring WiFi connectivity\n')
    for i, sta in enumerate(Ms):
        sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap{i + 1}')
    for i, sta in enumerate(Zs):
        sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap{i + 1}')
    for i, sta in enumerate(Ds):
        sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap{i + 1}')
    for i, sta in enumerate(WLCAMs):
        sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap{i + 1}')

    info('*** Assigning static routes\n')
    for i, sta in enumerate(Ms):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.{i+1}.1 netmask 255.255.0.0 up')
    for i, sta in enumerate(Zs):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.{i+1}.2 netmask 255.255.0.0 up')
    for i, sta in enumerate(Ds):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.{i+1}.3 netmask 255.255.0.0 up')
    for i, sta in enumerate(WLCAMs):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.{i+1}.5 netmask 255.255.0.0 up')

    server.cmd('ifconfig server-eth0 10.0.0.200 netmask 255.255.0.0 up')
    Ms[0].cmd('ifconfig m1-eth0 10.0.1.1 netmask 255.255.0.0 up')

    for i, sta in enumerate(WCAMs):
        sta.cmd(f'ifconfig {sta.name}-eth0 10.0.{i+1}.4 netmask 255.255.0.0 up')

    # Function to ping nodes and measure time
    def ping_node(node, target_ip):
        start_time = time.time()  # Record the start time
        node.cmd(f'ping -c 3 {target_ip}')  # Ping the target IP (e.g., server)
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        info(f"{node.name} pinged {target_ip} in {elapsed_time:.2f} seconds\n")  # Print the time taken

    # Pinging for each category of devices
    for node in Ms:
        ping_node(node, '10.0.0.200')  # Ping the server or any node you want as the target
    for node in Zs:
        ping_node(node, '10.0.0.200')
    for node in Ds:
        ping_node(node, '10.0.0.200')
    for node in WCAMs:
        ping_node(node, '10.0.0.200')
    for node in WLCAMs:
        ping_node(node, '10.0.0.200')

    # Optionally, you can ping again with a single ping (as per your original code)
    for node in Ms:
        ping_node(node, '10.0.0.200')  # Single ping to server or target

    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
