# import the topology creater class in Mininet
from mininet.topo import Topo
# create the class for creation of custom topology
class Lab4(Topo):
	# define constructor
	def __init__(self):
		# call super class constructor
		Topo.__init__(self)
		# add nodes
		host1 = self.addHost('H1')
		host2 = self.addHost('H2')
		host3 = self.addHost('H3')
		host4 = self.addHost('H4')
		switchC = self.addSwitch('S3')
		switchD = self.addSwitch('S4')
		switchE = self.addSwitch('S5')
		# add links
		self.addLink(host1, switchC, port2 = 1)
		self.addLink(host3, switchC, port2 = 2)
		self.addLink(host2, switchD, port2 = 1)
		self.addLink(host4, switchD, port2 = 2)
		self.addLink(switchC, switchD, port1 = 3, port2 = 3)
		self.addLink(switchC, switchE, port1 = 4, port2 = 1)
		self.addLink(switchD, switchE, port1 = 4, port2 = 2)

topos = {'Lab4' : (lambda : Lab4())}
