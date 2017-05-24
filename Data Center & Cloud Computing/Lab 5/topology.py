# import the topology creater class in Mininet
from mininet.topo import Topo
# create the class for creation of custom topology
class Lab5(Topo):
	# define constructor
	def __init__(self):
		# call super class constructor
		Topo.__init__(self)
		# add nodes
		host1 = self.addHost('H1')
		host2 = self.addHost('H2')
		switch1 = self.addSwitch('S1')
		# add links
		self.addLink(host1, switch1)
		self.addLink(host2, switch1)

topos = {'Lab5' : (lambda : Lab5())}