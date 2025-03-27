#!/usr/bin/python

from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, RemoteController

def topology():
    net = Containernet()

    info("*** Adding controller\n")
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

    info('*** Adding Docker Stations (IoT Devices with Different CPU Limits)\n')
    stations = []
    for i in range(1, 31):
        # Custom CPU limits based on type
        if i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:  # IoT-LAB M3
            cpu_limit = "0.1"
        elif i in [11, 12, 13, 14, 15 , 16, 17, 18, 19, 20]:  # Zolertia Firefly
            cpu_limit = "0.2"
        else:  # Decawave DWM1001
            cpu_limit = "0.3"

        sta = net.addStation(
            f'sta{i}',
            ip=f'10.0.0.{i}',
            mac=f'00:02:00:00:00:0{i}',
            cls=DockerSta,
            dimage="mininet-wifi-custom",
            cpus=cpu_limit
        )
        stations.append(sta)

    info("*** Adding host (Network Server)\n")
    server = net.addDocker('server', ip='10.0.0.200', dimage="mininet-wifi-custom", cpus="1")

    info("*** Adding Surveillance Cameras (High CPU Usage)\n")
    camera1 = net.addDocker('camera1', ip='10.0.0.101', dimage="mininet-wifi-custom", cpus="0.5")
    camera2 = net.addStation('camera2', ip='10.0.0.102', mac=f'00:02:00:00:01:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera3 = net.addDocker('camera3', ip='10.0.0.103', dimage="mininet-wifi-custom", cpus="0.5")
    camera4 = net.addStation('camera4', ip='10.0.0.104', mac=f'00:02:00:00:02:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera5 = net.addDocker('camera5', ip='10.0.0.105', dimage="mininet-wifi-custom", cpus="0.5")
    camera6 = net.addStation('camera6', ip='10.0.0.106', mac=f'00:02:00:00:03:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera7 = net.addDocker('camera7', ip='10.0.0.107', dimage="mininet-wifi-custom", cpus="0.5")
    camera8 = net.addStation('camera8', ip='10.0.0.108', mac=f'00:02:00:00:04:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera9 = net.addDocker('camera9', ip='10.0.0.109', dimage="mininet-wifi-custom", cpus="0.5")
    camera10 = net.addStation('camera10', ip='10.0.0.110', mac=f'00:02:00:00:05:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")   
    camera11 = net.addDocker('camera11', ip='10.0.0.111', dimage="mininet-wifi-custom", cpus="0.5")
    camera12 = net.addStation('camera12', ip='10.0.0.112', mac=f'00:02:00:00:06:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera13 = net.addDocker('camera13', ip='10.0.0.113', dimage="mininet-wifi-custom", cpus="0.5")
    camera14 = net.addStation('camera14', ip='10.0.0.114', mac=f'00:02:00:00:07:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera15 = net.addDocker('camera15', ip='10.0.0.115', dimage="mininet-wifi-custom", cpus="0.5")
    camera16 = net.addStation('camera16', ip='10.0.0.116', mac=f'00:02:00:00:08:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera17 = net.addDocker('camera17', ip='10.0.0.117', dimage="mininet-wifi-custom", cpus="0.5")
    camera18 = net.addStation('camera18', ip='10.0.0.118', mac=f'00:02:00:00:09:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")
    camera19 = net.addDocker('camera19', ip='10.0.0.119', dimage="mininet-wifi-custom", cpus="0.5")
    camera20 = net.addStation('camera20', ip='10.0.0.120', mac=f'00:02:00:00:010:00', cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.5")   

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

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

    # Connect stations to access points (up to 30 stations, scaled)
    for i in range(30):
        ap = f'ap{(i // 3) + 1}'  # Distribute stations evenly to APs
        net.addLink(stations[i], eval(ap), cls=TCLink, delay='50ms', bw=1)

    # Core network connections
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

    # Surveillance camera links
    net.addLink(camera1, ap1, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera2, ap1, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera3, ap2, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera4, ap2, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera5, ap3, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera6, ap3, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera7, ap4, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera8, ap4, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera9, ap5, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera10, ap5, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera11, ap6, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera12, ap6, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera13, ap7, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera14, ap7, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera15, ap8, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera16, ap8, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera17, ap9, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera18, ap9, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera19, ap10, cls=TCLink, delay='50ms', bw=5)
    net.addLink(camera20, ap10, cls=TCLink, delay='50ms', bw=5)

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

    info('*** Ensuring WiFi connectivity\n')
    for i, sta in enumerate(stations):
        sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap{(i // 3) + 1}')

    camera2.cmd('iw dev camera2-wlan0 connect ssid-ap1')
    camera4.cmd('iw dev camera4-wlan0 connect ssid-ap2')
    camera6.cmd('iw dev camera6-wlan0 connect ssid-ap3')
    camera8.cmd('iw dev camera8-wlan0 connect ssid-ap4')
    camera10.cmd('iw dev camera10-wlan0 connect ssid-ap5')
    camera12.cmd('iw dev camera12-wlan0 connect ssid-ap6')
    camera14.cmd('iw dev camera14-wlan0 connect ssid-ap7')
    camera16.cmd('iw dev camera16-wlan0 connect ssid-ap8')
    camera18.cmd('iw dev camera18-wlan0 connect ssid-ap9')
    camera20.cmd('iw dev camera20-wlan0 connect ssid-ap10')

    info('*** Assigning static routes \n')
    for i, sta in enumerate(stations):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.0.{i+1} netmask 255.255.255.0 up')

    camera2.cmd('ifconfig camera2-wlan0 10.0.0.102 netmask 255.255.255.0 up')
    camera4.cmd('ifconfig camera4-wlan0 10.0.0.104 netmask 255.255.255.0 up')
    camera6.cmd('ifconfig camera6-wlan0 10.0.0.106 netmask 255.255.255.0 up')
    camera8.cmd('ifconfig camera8-wlan0 10.0.0.108 netmask 255.255.255.0 up')
    camera10.cmd('ifconfig camera10-wlan0 10.0.0.110 netmask 255.255.255.0 up')
    camera12.cmd('ifconfig camera12-wlan0 10.0.0.112 netmask 255.255.255.0 up')
    camera14.cmd('ifconfig camera14-wlan0 10.0.0.114 netmask 255.255.255.0 up')
    camera16.cmd('ifconfig camera16-wlan0 10.0.0.116 netmask 255.255.255.0 up')
    camera18.cmd('ifconfig camera18-wlan0 10.0.0.118 netmask 255.255.255.0 up')
    camera20.cmd('ifconfig camera20-wlan0 10.0.0.120 netmask 255.255.255.0 up')

    server.cmd('ifconfig server-eth0 10.0.0.200 netmask 255.255.255.0 up')

    camera1.cmd('ifconfig camera1-eth0 10.0.0.101 netmask 255.255.255.0 up')
    camera3.cmd('ifconfig camera3-eth0 10.0.0.103 netmask 255.255.255.0 up')
    camera5.cmd('ifconfig camera5-eth0 10.0.0.105 netmask 255.255.255.0 up')
    camera7.cmd('ifconfig camera7-eth0 10.0.0.107 netmask 255.255.255.0 up')
    camera9.cmd('ifconfig camera9-eth0 10.0.0.109 netmask 255.255.255.0 up')
    camera11.cmd('ifconfig camera11-eth0 10.0.0.111 netmask 255.255.255.0 up')
    camera13.cmd('ifconfig camera13-eth0 10.0.0.113 netmask 255.255.255.0 up')
    camera15.cmd('ifconfig camera15-eth0 10.0.0.115 netmask 255.255.255.0 up')
    camera17.cmd('ifconfig camera17-eth0 10.0.0.117 netmask 255.255.255.0 up')
    camera19.cmd('ifconfig camera19-eth0 10.0.0.119 netmask 255.255.255.0 up')

    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
