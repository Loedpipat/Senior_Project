#!/usr/bin/python

from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller, RemoteController

def topology():
    net = Containernet()

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.201', port=6633)
    
    info("*** Adding Access Points\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='10,20,0')

    info("*** Adding OpenFlow switches\n")
    s1 = net.addSwitch('s1')

    info('*** Adding docker containers\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', mac='00:02:00:00:00:01',
                          cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=20)
    sta2 = net.addStation('sta2', ip='10.0.0.2', mac='00:02:00:00:00:02',
                          cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=20)
    
    info("*** Adding host\n")
    h1 = net.addDocker('h1', ip='10.0.0.10', dimage="ubuntu:trusty")

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

    info('*** Creating links\n')
    net.addLink(ap1, s1)

    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    net.addLink(s1, h1)

    info('*** Starting network\n')
    net.start()
    c0.start()
    ap1.start([c0])
    s1.start([c0])

    makeTerm(sta1, cmd="bash -c 'apt-get update && apt-get install iw wireless-tools ethtool iproute2 net-tools -y;'")
    makeTerm(sta2, cmd="bash -c 'apt-get update && apt-get install iw wireless-tools ethtool iproute2 net-tools -y;'")

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

