#!/usr/bin/python

from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mininet.link import TCLink
from mn_wifi.wmediumdConnector import interference
from mininet.log import setLogLevel, info

def setup_network():
    # Create the Mininet-WiFi network
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

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

    info("*** Adding stations (IoT nodes)\n")
    m1 = net.addStation('m1', ip='10.0.0.1/24', position='20,20,0')
    m2 = net.addStation('m2', ip='10.0.0.2/24', position='20,30,10')
    m3 = net.addStation('m3', ip='10.0.0.3/24', position='20,20,20')

    z1 = net.addStation('z1', ip='10.0.0.4/24', position='20,30,0')
    z2 = net.addStation('z2', ip='10.0.0.5/24', position='20,30,10')
    z3 = net.addStation('z3', ip='10.0.0.6/24', position='20,30,20')

    d1 = net.addStation('d1', ip='10.0.0.7/24', position='20,30,0')
    d2 = net.addStation('d2', ip='10.0.0.8/24', position='20,30,10')
    d3 = net.addStation('d3', ip='10.0.0.9/24', position='20,30,20')


    info("*** Adding a host\n")
    h1 = net.addHost('h1', ip='10.0.0.10/24')

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, s1, cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap2, s2, cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap3, s3, cls=TCLink, delay='50ms', bw=10)

    # Connect stations to access points
    net.addLink(m1, ap1)
    net.addLink(z1, ap1)
    net.addLink(d1, ap1)

    net.addLink(m2, ap2)
    net.addLink(z2, ap2)
    net.addLink(d2, ap2)

    net.addLink(m3, ap3)
    net.addLink(z3, ap3)
    net.addLink(d3, ap3)

    # Connect switches
    net.addLink(s1, s4, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s2, s4, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s3, s5, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s4, s6, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s5, s7, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s6, s8, cls=TCLink, delay='50ms', bw=10)
    net.addLink(s7, s8, cls=TCLink, delay='50ms', bw=10)
    
    # Connect host
    net.addLink(h1, s8, cls=TCLink, delay='50ms', bw=10)

    info("*** Starting network\n")
    net.build()
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

    info("*** Connecting stations to APs automatically\n")
    m1.cmd(f'iw dev m1-wlan0 connect ssid-ap1')
    z1.cmd(f'iw dev z1-wlan0 connect ssid-ap1')
    d1.cmd(f'iw dev d1-wlan0 connect ssid-ap1')

    m2.cmd(f'iw dev m2-wlan0 connect ssid-ap2')
    z2.cmd(f'iw dev z2-wlan0 connect ssid-ap2')
    d2.cmd(f'iw dev d2-wlan0 connect ssid-ap2')

    m3.cmd(f'iw dev m3-wlan0 connect ssid-ap3')
    z3.cmd(f'iw dev z3-wlan0 connect ssid-ap3')
    d3.cmd(f'iw dev d3-wlan0 connect ssid-ap3')

    info("*** Assigning IPv4 addresses to WLAN interfaces\n")
    m1.cmd(f'ip addr add 10.0.0.1/24 dev m1-wlan0')
    m2.cmd(f'ip addr add 10.0.0.2/24 dev m2-wlan0')
    m3.cmd(f'ip addr add 10.0.0.3/24 dev m3-wlan0')
    
    z1.cmd(f'ip addr add 10.0.0.4/24 dev z1-wlan0')
    z2.cmd(f'ip addr add 10.0.0.5/24 dev z2-wlan0')
    z3.cmd(f'ip addr add 10.0.0.6/24 dev z3-wlan0')
    
    d1.cmd(f'ip addr add 10.0.0.7/24 dev d1-wlan0')
    d2.cmd(f'ip addr add 10.0.0.8/24 dev d2-wlan0')
    d3.cmd(f'ip addr add 10.0.0.9/24 dev d3-wlan0')

    h1.cmd('ip addr add 10.0.0.10/24 dev h1-eth0')

    info("*** Setting TX Power\n")
    m1.setTxPower(3, intf='m1-wlan0')
    m2.setTxPower(3, intf='m2-wlan0')
    m3.setTxPower(3, intf='m3-wlan0')

    z1.setTxPower(5, intf='z1-wlan0')
    z2.setTxPower(5, intf='z2-wlan0')
    z3.setTxPower(5, intf='z3-wlan0')

    d1.setTxPower(10, intf='d1-wlan0')
    d2.setTxPower(10, intf='d2-wlan0')
    d3.setTxPower(10, intf='d3-wlan0')


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()
