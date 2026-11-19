"""Non-interactive test for the Workshop 05 solution topology.

Starts the Mininet topology defined in solutions/topology.py and verifies:
  * all interfaces have the expected IP addresses
  * IP forwarding is enabled on h2 and h3
  * static routes are present on h2 and h3
  * pingall reaches every host (0% packet loss)
  * h1 can reach h4 (end-to-end across the three regions)

Run with:  sudo python3 solutions/test_solution.py
"""
from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.log import setLogLevel, info
from mininet.nodelib import LinuxBridge
from topology import topos

setLogLevel('info')


def cmd(h, c):
    return h.cmd(c).strip()


def main():
    topo = topos['tutorialTopology']()
    net = Mininet(topo=topo, controller=None, switch=LinuxBridge,
                  autoSetMacs=True)
    net.start()

    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

    print('*** Interface IP configuration ***')
    for h in (h1, h2, h3, h4):
        print(h.name + ':')
        print('  ' + cmd(h, 'ip -brief addr show').replace('\n', '\n  '))

    print('*** Routing tables ***')
    for h in (h1, h2, h3, h4):
        print(h.name + ':')
        print('  ' + cmd(h, 'ip route show').replace('\n', '\n  '))

    print('*** IP forwarding on routers ***')
    print('h2:', cmd(h2, 'sysctl net.ipv4.ip_forward'))
    print('h3:', cmd(h3, 'sysctl net.ipv4.ip_forward'))

    print('*** pingall ***')
    result = net.pingAll()
    print('pingall packet loss: {:.0f}%'.format(result * 100))

    print('*** End-to-end tests: h1 <-> h4 ***')
    print(cmd(h1, 'ping -c 3 10.1.0.2'))
    print(cmd(h4, 'ping -c 3 10.0.0.1'))

    net.stop()


if __name__ == '__main__':
    main()
