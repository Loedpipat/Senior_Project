#!/usr/bin/python

from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.link import TCLink
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller, RemoteController

def topology():
    net = Containernet()

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.201', port=6633)
    
    info("*** Adding Access Points\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='10,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='10,20,10')
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11', position='10,20,20')

    info("*** Adding OpenFlow switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')
    s8 = net.addSwitch('s8')

    info('*** Adding docker containers\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', mac='00:02:00:00:00:01', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta2 = net.addStation('sta2', ip='10.0.0.2', mac='00:02:00:00:00:02', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta3 = net.addStation('sta3', ip='10.0.0.3', mac='00:02:00:00:00:03', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)

    sta4 = net.addStation('sta4', ip='10.0.0.4', mac='00:02:00:00:00:04', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta5 = net.addStation('sta5', ip='10.0.0.5', mac='00:02:00:00:00:05', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta6 = net.addStation('sta6', ip='10.0.0.6', mac='00:02:00:00:00:06', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)

    sta7 = net.addStation('sta7', ip='10.0.0.7', mac='00:02:00:00:00:07', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta8 = net.addStation('sta8', ip='10.0.0.8', mac='00:02:00:00:00:08', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)
    sta9 = net.addStation('sta9', ip='10.0.0.9', mac='00:02:00:00:00:09', cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=10)

    info("*** Adding host\n")
    h1 = net.addDocker('h1', ip='10.0.0.10', dimage="ubuntu:trusty")

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

    info('*** Creating links\n')
    net.addLink(ap1, s1, cls=TCLink, delay='100ms', bw=10)
    net.addLink(ap2, s2, cls=TCLink, delay='100ms', bw=10)
    net.addLink(ap3, s3, cls=TCLink, delay='100ms', bw=10)

    net.addLink(sta1, ap1, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta2, ap1, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta3, ap1, cls=TCLink, delay='100ms', bw=1)

    net.addLink(sta4, ap2, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta5, ap2, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta6, ap2, cls=TCLink, delay='100ms', bw=1)

    net.addLink(sta7, ap3, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta8, ap3, cls=TCLink, delay='100ms', bw=1)
    net.addLink(sta9, ap3, cls=TCLink, delay='100ms', bw=1)  

    net.addLink(s1, s4, cls=TCLink, delay='100ms', bw=10)
    net.addLink(s2, s4, cls=TCLink, delay='100ms', bw=10)
    net.addLink(s3, s5, cls=TCLink, delay='100ms', bw=10)
    
    net.addLink(s4, s6, cls=TCLink, delay='100ms', bw=10)
    net.addLink(s5, s7, cls=TCLink, delay='100ms', bw=10)
    net.addLink(s6, s8, cls=TCLink, delay='100ms', bw=10)
    net.addLink(s7, s8, cls=TCLink, delay='100ms', bw=10)

    net.addLink(h1, s8, cls=TCLink, delay='100ms', bw=10)  

    info('*** Starting network\n')
    net.start()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])
    s5.start([c0])
    s6.start([c0])
    s7.start([c0])
    s8.start([c0])
    
    sta1.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta2.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta3.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta4.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta5.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta6.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta7.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta8.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")
    sta9.cmd("apt-get update && apt-get install -y iw wireless-tools ethtool iproute2 net-tools")

    sta1.cmd('iw dev sta1-wlan0 connect ssid-ap1')
    sta2.cmd('iw dev sta2-wlan0 connect ssid-ap1')
    sta3.cmd('iw dev sta3-wlan0 connect ssid-ap1')

    sta4.cmd('iw dev sta4-wlan0 connect ssid-ap2')
    sta5.cmd('iw dev sta5-wlan0 connect ssid-ap2')
    sta6.cmd('iw dev sta6-wlan0 connect ssid-ap2')

    sta7.cmd('iw dev sta7-wlan0 connect ssid-ap3')
    sta8.cmd('iw dev sta8-wlan0 connect ssid-ap3')
    sta9.cmd('iw dev sta9-wlan0 connect ssid-ap3')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

