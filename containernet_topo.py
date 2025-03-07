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

    info("*** Adding OpenFlow switches\n")
    switches = {f's{i}': net.addSwitch(f's{i}') for i in range(1, 9)}

    info('*** Adding Docker Stations (Limited CPU Usage)\n')
    stations = []
    for i in range(1, 10):
        sta = net.addStation(f'sta{i}', ip=f'10.0.0.{i}', mac=f'00:02:00:00:00:0{i}',
                             cls=DockerSta, dimage="mininet-wifi-custom", cpus="0.2")
        stations.append(sta)

    info("*** Adding host\n")
    h1 = net.addDocker('h1', ip='10.0.0.10', dimage="mininet-wifi-custom")

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

    info('*** Creating links\n')
    net.addLink(ap1, switches['s1'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap2, switches['s2'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap3, switches['s3'], cls=TCLink, delay='50ms', bw=10)

    # Connect stations to access points
    for i in range(3):
        net.addLink(stations[i], ap1, cls=TCLink, delay='50ms', bw=1)
        net.addLink(stations[i+3], ap2, cls=TCLink, delay='50ms', bw=1)
        net.addLink(stations[i+6], ap3, cls=TCLink, delay='50ms', bw=1)

    # Core network connections
    net.addLink(switches['s1'], switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s2'], switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s3'], switches['s5'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s4'], switches['s6'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s5'], switches['s7'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s6'], switches['s8'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s7'], switches['s8'], cls=TCLink, delay='50ms', bw=10)

    net.addLink(h1, switches['s8'], cls=TCLink, delay='50ms', bw=10)

    info('*** Starting network\n')
    net.start()
    c0.start()

    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    for s in switches.values():
        s.start([c0])

    info('*** Ensuring WiFi connectivity\n')
    for i, sta in enumerate(stations):
        if i < 3:
            sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap1')
        elif i < 6:
            sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap2')
        else:
            sta.cmd(f'iw dev {sta.name}-wlan0 connect ssid-ap3')

    info('*** Assigning static routes (Avoids Unreachable Errors)\n')
    for i, sta in enumerate(stations):
        sta.cmd(f'ifconfig {sta.name}-wlan0 10.0.0.{i+1} netmask 255.255.255.0 up')

    h1.cmd('ifconfig h1-eth0 10.0.0.10 netmask 255.255.255.0 up')

    info('*** Verifying connectivity\n')
    for sta in stations:
        result = sta.cmd(f'ping -c 3 10.0.0.10')
        info(result)

    info('Pingall completed')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
