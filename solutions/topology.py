from mininet.topo import Topo
from mininet.node import Node


class LinuxRouter(Node):
    """A host that acts as a router: IP forwarding on, static routes supported."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable IP forwarding so this host can forward packets between regions
        self.cmd('sysctl net.ipv4.ip_forward=1')
        # Add static routes passed via the 'routes' parameter:
        # routes=[('10.1.0.0/24', '192.168.0.2'), ...]
        if 'routes' in params:
            for (ip, gateway) in params['routes']:
                self.cmd('ip route add {} via {}'.format(ip, gateway))

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class TutorialTopology(Topo):

    def build(self):
        # --- Hosts with embedded IP configuration ---
        # Region 1 (10.0.0.0/24): h1 <--> h2
        h1 = self.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.2')
        # h2 acts as a router between Region 1 and Region 2
        h2 = self.addHost('h2', cls=LinuxRouter, ip='10.0.0.2/24',
                          routes=[('10.1.0.0/24', '192.168.0.2')])
        # h3 acts as a router between Region 2 and Region 3
        h3 = self.addHost('h3', cls=LinuxRouter, ip='192.168.0.2/24',
                          routes=[('10.0.0.0/24', '192.168.0.1')])
        # Region 3 (10.1.0.0/24): h3 <--> h4
        h4 = self.addHost('h4', ip='10.1.0.2/24', defaultRoute='via 10.1.0.1')

        # --- Switches ---
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # --- Links with realism (bandwidth, delay, loss) ---
        # Region 1 access links: h1 <--> s1 <--> h2
        self.addLink(h1, s1, bw=100, delay='30ms', loss=1)
        self.addLink(s1, h2, bw=10, delay='10ms', loss=1)
        # Router inter-connect link: h2 <--> h3 (Region 2, 192.168.0.0/24)
        self.addLink(h2, h3, intfName1='h2-eth1', params1={'ip': '192.168.0.1/24'},
                     intfName2='h3-eth0', params2={'ip': '192.168.0.2/24'})
        # Region 3 access links: h4 <--> s2 <--> h3
        self.addLink(h4, s2, bw=100, delay='100ms')
        self.addLink(s2, h3, bw=100, delay='100ms', intfName2='h3-eth1',
                     params2={'ip': '10.1.0.1/24'})


# the topologies accessible to the mn tool's `--topo` flag
# note: if using the Dockerfile, this must be the same as in the Dockerfile
topos = {'tutorialTopology': (lambda: TutorialTopology())}
