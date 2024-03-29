from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether
from ryu.ofproto import inet
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
# you may import more libs here, but the above libs should be enough

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        # arp table: for searching
        self.arp_table={}
        # fill in the table for arp searching
        self.arp_table["10.0.0.1"] = "00:00:00:00:00:01"
        self.arp_table["10.0.0.2"] = "00:00:00:00:00:02"
        self.arp_table["10.0.0.3"] = "00:00:00:00:00:03"
        self.arp_table["10.0.0.4"] = "00:00:00:00:00:04"

    """
        Hand-shake event call back method
        This is the very initial method where the switch hand shake with the controller
        It checks whether both are using the same protocol version: OpenFlow 1.3 in this case

        Therefore in this method, you can setup some static rules.
        e.g. the rules which sends unknown packets to the controller 
             the rules directing TCP/UDP/ICMP traffic
             ACL rules
    """
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Insert Static rule
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # Installing static rules to process TCP/UDP and ICMP and ACL
        dpid = datapath.id  # classifying the switch ID
        if dpid == 3:
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.1', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.3', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.2', 10, 3) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.4', 10, 3) # change

            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.1', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.3', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.2', 10, 3) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.4', 10, 3) # change

            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.1', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.3', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.2', 10, 4) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.4', 10, 4) # change

            # implement ACL rules
            # this rule directs the TCP packets from h1 to h3 to the controller
            match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,
                                    ipv4_src = '10.0.0.1',
                                    ipv4_dst = '10.0.0.3',
                                    ip_proto = inet.IPPROTO_TCP)
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 30, match, actions)

        elif dpid == 4:
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.2', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.4', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.1', 10, 3) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_TCP, '10.0.0.3', 10, 3) # change

            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.2', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.4', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.1', 10, 3) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_ICMP, '10.0.0.3', 10, 3) # change

            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.2', 10, 1) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.4', 10, 2) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.1', 10, 4) # change
            self.add_layer4_rules(datapath, inet.IPPROTO_UDP, '10.0.0.3', 10, 4) # change

        elif dpid == 5:
            # fwding everthing between port 1 and port 2
            actions = [parser.OFPActionOutput(2)]
            match = parser.OFPMatch(in_port = 1,
                                    eth_type = ether.ETH_TYPE_IP)
            self.add_flow(datapath, 10, match, actions)
            actions = [parser.OFPActionOutput(1)]
            match = parser.OFPMatch(in_port = 2,
                                    eth_type = ether.ETH_TYPE_IP)
            self.add_flow(datapath, 10, match, actions)
            
            match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,
                                    ipv4_src = '10.0.0.2',
                                    ipv4_dst = '10.0.0.3',
                                    ip_proto = inet.IPPROTO_UDP)
            actions = []
            self.add_flow(datapath, 30, match, actions)

        else:
            print "wrong switch"
    

    """ 
        Call back method for PacketIn Message
        This is the call back method when a PacketIn Msg is sent
        from a switch to the controller
        It handles L3 classification in this function:
    """ 
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ethertype = eth.ethertype

        # process ARP 
        if ethertype == ether.ETH_TYPE_ARP:
            self.handle_arp(datapath, in_port, pkt)
            return

        # process IP
        if ethertype == ether.ETH_TYPE_IP:
            self.handle_ip(datapath, in_port, pkt)
            return

    # Member methods you can call to install TCP/UDP/ICMP fwding rules
    def add_layer4_rules(self, datapath, ip_proto, ipv4_dst = None, priority = 1, fwd_port = None):
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(fwd_port)]
        match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,
                                ip_proto = ip_proto,
                                ipv4_dst = ipv4_dst)
        self.add_flow(datapath, priority, match, actions)

    # Member methods you can call to install general rules
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    """
        Methods to handle ARP. In this implementation the controller
        generates the ARP reply msg back to the host who initiate it.
        So the controller should parse out the ARP request;
        Search the ARP table for correponding dst MAC;
        Generate ARP reply;
        And finally use PacketOut Message to send back the ARP reply
    """
    def handle_arp(self, datapath, in_port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # parse out the ethernet and arp packet
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        arp_pkt = pkt.get_protocol(arp.arp)
        # obtain the MAC of dst IP  
        arp_resolv_mac = self.arp_table[arp_pkt.dst_ip]

        ether_hd = ethernet.ethernet(dst = eth_pkt.src, 
                                    src = arp_resolv_mac,
                                    ethertype = ether.ETH_TYPE_ARP);
        arp_hd = arp.arp(hwtype = 1, proto = 0x0800, hlen = 6, plen = 4,
                        opcode = 2, src_mac = arp_resolv_mac, src_ip = arp_pkt.dst_ip,
                        dst_mac = eth_pkt.src, dst_ip = arp_pkt.src_ip)
        arp_reply = packet.Packet();
        arp_reply.add_protocol(ether_hd)
        arp_reply.add_protocol(arp_hd)
        arp_reply.serialize()
        
        # send the Packet Out mst to back to the host who is initilaizing the ARP
        actions = [parser.OFPActionOutput(in_port)];
        out = parser.OFPPacketOut(datapath, ofproto.OFP_NO_BUFFER, 
                                  ofproto.OFPP_CONTROLLER, actions,
                                  arp_reply.data)
        datapath.send_msg(out)

    """
        Methods to handle TCP/IP. In this implementation the controller
        generate the TCP RST for connections between h1 and h3.
        In switch_features_handler() you should put a static rule to fwd 
        those packets to the controller, and in handle_ip() you need to 
        generate and return the TCP RST with PacketOut Message
    """
    def handle_ip(self, datapath, in_port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        ipv4_pkt = pkt.get_protocol(ipv4.ipv4) # parse out the IPv4 pkt

        if datapath.id == 3 and ipv4_pkt.proto == inet.IPPROTO_TCP:
            tcp_pkt = pkt.get_protocol(tcp.tcp) # parser out the TCP pkt

            ### generate the TCP packet with the RST flag set to 1
            ### packet generation is similar to ARP,
            ### but you need to generate ethernet->ip->tcp and serialize it

            ether_frame = ethernet.ethernet(dst = self.arp_table[ipv4_pkt.src], 
                                    src = self.arp_table[ipv4_pkt.dst],
                                    ethertype = ether.ETH_TYPE_IP)
            ip_packet = ipv4.ipv4(version = 4, header_length = 5, tos = 0,
                        total_length = 0, identification = 0, flags = 0,
                        offset = 0, ttl = 255, proto = 0x06, csum = 0,
                        src = ipv4_pkt.dst, dst = ipv4_pkt.src, option = None)
            tcp_segment = tcp.tcp(src_port = tcp_pkt.dst_port, dst_port = tcp_pkt.src_port, seq = 0,
                                ack = (tcp_pkt.seq + 1), offset = 0, bits = 0x004, window_size = 0, csum = 0,
                                urgent = 0, option = None)

            tcp_rst_ack = packet.Packet();
            tcp_rst_ack.add_protocol(ether_frame)
            tcp_rst_ack.add_protocol(ip_packet)
            tcp_rst_ack.add_protocol(tcp_segment)
            tcp_rst_ack.serialize()
            
        # send the Packet Out mst to back to the host who is initilaizing the ARP
            actions = [parser.OFPActionOutput(in_port)];
            out = parser.OFPPacketOut(datapath, ofproto.OFP_NO_BUFFER, 
                                      ofproto.OFPP_CONTROLLER, actions,
                                      tcp_rst_ack.data)
            datapath.send_msg(out)
