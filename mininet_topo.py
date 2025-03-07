#!/usr/bin/python

import os
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mininet.link import TCLink
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import UserAP
from mininet.log import setLogLevel, info

def setup_network():
    net = Mininet_wifi(controller=Controller, link=TCLink, wmediumd_mode=interference)

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.201', port=6633)

    info("*** Adding Access Points (Using UserAP for `wmediumd` support)\n")
    ap1 = net.addAccessPoint('ap1', cls=UserAP, ssid='ssid-ap1', mode='g', channel='1', position='10,20,0', range=120, txpower=3)
    ap2 = net.addAccessPoint('ap2', cls=UserAP, ssid='ssid-ap2', mode='g', channel='6', position='10,20,10', range=120, txpower=3)
    ap3 = net.addAccessPoint('ap3', cls=UserAP, ssid='ssid-ap3', mode='g', channel='11', position='10,20,20', range=120, txpower=3)

    info("*** Adding OpenFlow switches\n")
    switches = {f's{i}': net.addSwitch(f's{i}') for i in range(1, 9)}

    info("*** Adding stations (IoT nodes)\n")
    stations = {
        'm1': net.addStation('m1', ip='10.0.0.1/24', position='20,20,0'),
        'm2': net.addStation('m2', ip='10.0.0.2/24', position='20,30,10'),
        'm3': net.addStation('m3', ip='10.0.0.3/24', position='20,20,20'),
        'z1': net.addStation('z1', ip='10.0.0.4/24', position='20,30,0'),
        'z2': net.addStation('z2', ip='10.0.0.5/24', position='20,30,10'),
        'z3': net.addStation('z3', ip='10.0.0.6/24', position='20,30,20'),
        'd1': net.addStation('d1', ip='10.0.0.7/24', position='20,30,0'),
        'd2': net.addStation('d2', ip='10.0.0.8/24', position='20,30,10'),
        'd3': net.addStation('d3', ip='10.0.0.9/24', position='20,30,20')
    }

    info("*** Adding a host\n")
    h1 = net.addHost('h1', ip='10.0.0.10/24')

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Preventing Auto Association on APs\n")
    net.auto_association = lambda: None  # Disables auto association properly

    info("*** Setting AP Positions for `wmediumd`\n")
    for ap in [ap1, ap2, ap3]:
        ap.params['position'] = [float(x) for x in ap.params.get('position', ['0', '0', '0'])]
        ap.lastpos = ap.params['position']
        ap.coord = ap.params['position']
        ap.setPosition(f"{ap.params['position'][0]},{ap.params['position'][1]},{ap.params['position'][2]}")

    info("*** Bringing Up WiFi Interfaces and Auto-Associating Stations\n")
    for sta_name, sta in stations.items():
        sta.cmd(f"ifconfig {sta_name}-wlan0 up")  # Ensure wlan0 is up
        sta.cmd(f"ifconfig {sta_name}-wlan0 down && ifconfig {sta_name}-wlan0 up")  # Restart if needed

        # Associate stations with correct APs
        if sta_name in ['m1', 'z1', 'd1']:
            sta.cmd(f"iw dev {sta_name}-wlan0 connect ssid-ap1")
        elif sta_name in ['m2', 'z2', 'd2']:
            sta.cmd(f"iw dev {sta_name}-wlan0 connect ssid-ap2")
        elif sta_name in ['m3', 'z3', 'd3']:
            sta.cmd(f"iw dev {sta_name}-wlan0 connect ssid-ap3")

    info("*** Creating links\n")
    net.addLink(ap1, switches['s1'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap2, switches['s2'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(ap3, switches['s3'], cls=TCLink, delay='50ms', bw=10)

    net.addLink(switches['s1'], switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s2'], switches['s4'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s3'], switches['s5'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s4'], switches['s6'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s5'], switches['s7'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s6'], switches['s8'], cls=TCLink, delay='50ms', bw=10)
    net.addLink(switches['s7'], switches['s8'], cls=TCLink, delay='50ms', bw=10)

    net.addLink(h1, switches['s8'], cls=TCLink, delay='50ms', bw=10)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    for s in switches.values():
        s.start([c0])

    info("*** Assigning IPv4 addresses to WLAN interfaces\n")
    for sta_name, sta in stations.items():
        sta.cmd(f"ip addr add {sta.params['ip']} dev {sta_name}-wlan0")

    h1.cmd("ip addr add 10.0.0.10/24 dev h1-eth0")

    info("*** Generating IoT Traffic\n")
    stations['m1'].cmd('iperf -c 10.0.0.10 -u -b 2M -t 60 &')
    stations['m2'].cmd('iperf -c 10.0.0.10 -u -b 1M -t 60 &')
    stations['d1'].cmd('ping -c 10 10.0.0.10 > ping_log.txt &')

    info("*** Dumping OpenFlow Table\n")
    os.system("sudo ovs-ofctl dump-flows s1 > openflow_logs.txt")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()
