#!/usr/bin/python
"""
This is an example with Traffic Control for link weight.
"""
from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel


def topology():
    net = Containernet()

    info('*** Adding docker containers\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', mac='00:02:00:00:00:01',
                          cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=50)
    sta2 = net.addStation('sta2', ip='10.0.0.2', mac='00:02:00:00:00:02',
                          cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=50)
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1')
    c0 = net.addController('c0')

    info('*** Configuring WiFi nodes\n')
    net.configureWifiNodes()

    info('*** Starting network\n')
    net.start()

    # Update and install necessary packages in the Docker containers
    makeTerm(sta1, cmd="bash -c 'apt-get update && apt-get install -y iproute2 net-tools;'")
    makeTerm(sta2, cmd="bash -c 'apt-get update && apt-get install -y iproute2 net-tools;'")

    # Connect stations to the access point
    sta1.cmd('iw dev sta1-wlan0 connect new-ssid')
    sta2.cmd('iw dev sta2-wlan0 connect new-ssid')

    # Apply traffic control rules to control link weights
    info('*** Configuring Traffic Control (TC) for link weights\n')

    # Example: Apply 1 Mbps bandwidth limit between sta1 and ap1
    sta1.cmd('tc qdisc add dev sta1-wlan0 root tbf rate 1mbit burst 32kbit latency 400ms')

    # Example: Apply 2 Mbps bandwidth limit between sta2 and ap1
    sta2.cmd('tc qdisc add dev sta2-wlan0 root tbf rate 2mbit burst 32kbit latency 400ms')

    info('*** Running CLI\n')
    CLI(net)

    # Stop the network
    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
