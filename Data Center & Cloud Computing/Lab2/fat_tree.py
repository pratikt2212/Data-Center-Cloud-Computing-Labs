#Datacentre Topology example
from mininet.topo import Topo
class MyTopo (Topo) :

	def __init__(self):
		#initialize topology
		Topo.__init__(self)
		#add hosts and switches
		Host = [1,2,3,4,5,6,7,8]
		for i in range (0,8):
			Host[i] = self.addHost('H%s' % (i+1))
		C1 = self.addSwitch ( 'C1' )
		C2 = self.addSwitch ( 'C2' )
		E1 = self.addSwitch ( 'E1' )
		E2 = self.addSwitch ( 'E2' )
		E3 = self.addSwitch ( 'E3' )
		E4 = self.addSwitch ( 'E4' )
		# add links
		self.addLink ( Host[0] ,E1)
		self.addLink ( Host[1] ,E1)
		self.addLink ( E1,C1)
		self.addLink ( E1,C2)
		self.addLink ( Host[2] ,E2)
                self.addLink ( Host[3] ,E2)
		self.addLink ( E2,C1)
                self.addLink ( E1,C2)
		self.addLink ( Host[4] ,E3)
                self.addLink ( Host[5] ,E3)
		self.addLink ( E3,C2)
                self.addLink ( E3,C1)
		self.addLink ( Host[6] ,E4)
                self.addLink ( Host[7] ,E4)
		self.addLink ( E4,C2)
                self.addLink ( E4,C1)
topos = { 'mytopo' : ( lambda : MyTopo() ) }

