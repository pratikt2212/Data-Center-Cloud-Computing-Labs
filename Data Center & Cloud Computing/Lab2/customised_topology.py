from mininet.topo import Topo

class MyTopo(Topo):

        #Simple topology example

        def __init__(self):

                #Create custom Topo

                #Initialize Topology

                Topo.__init__(self)

                # Add Hosts and Switches

                h1 = self.addHost('h1')
                h2 = self.addHost('h2')
                s1 = self.addSwitch('s1')
                s2 = self.addSwitch('s2')
                s3 = self.addSwitch('s3')
                s4 = self.addSwitch('s4')

                # Add links

                self.addLink(h1,s1)
                self.addLink(s1,s2)
                self.addLink(s1,s3)
                self.addLink(s3,s4)
                self.addLink(s2,s4)
                self.addLink(s4,h2)

topos = {'mytopo':(lambda:MyTopo())}
