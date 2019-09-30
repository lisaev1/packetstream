#!python3
"""
Common subroutines for the streaming packet dissector
"""

#import sys, os
import scapy.all as scapy

def _is_netbios(pkt):
    """
    Test if a packet is one of NetBios types.

    Input:
        pkt -- scapy packet
    Return:
        True for NetBios; False otherwise
    """
    ports = (137, 138, 139)

    #-- first, we need only TCP (proto 0x6) or UDP (0x11) packets
    try:
        protocol = pkt.proto
    except AttributeError:
        return False

    if (protocol != 0x6) and (protocol != 0x11):
        return False
    elif (protocol == 0x6):
        p = pkt["TCP"]
    elif (protocol == 0x11):
        p = pkt["UDP"]

    if ((p.sport in ports) or (p.dport in ports)):
        return True

    return False


def _is_arp(pkt):
    """
    Test if a packet is ARP.

    Input:
        pkt -- scapy packet
    Return:
        True for ARP (0x806) and False otherwise
    """

    return (pkt.type == 0x806)


def _is_ssh(pkt):
    """
    Test if a packet is SSH.

    Input:
        pkt -- scapy packet
    Return:
        True for an SSH packet (source or destination port 22); False otherwise
    """
    #-- test that we have a TCP (proto 0x6) packet...
    try:
        protocol = pkt.proto
    except AttributeError:
        return False

    if (protocol != 0x6):
        return False

    #-- ... and if yes, test ports
    tcp_pkt = pkt["TCP"]

    if ((tcp_pkt.sport == 22) or (tcp_pkt.dport == 22)):
        return True
    
    return False


def _pkt_filter(pkt):
    """
    Filter out some common packet types, such as ARP. This function relies on
    external single-purpose subroutines that test individual ether types [1],
    e.g. _is_arp().
    [1] https://github.com/secdev/scapy/blob/master/scapy/modules/ethertypes.py

    Input:
        pkt -- scapy packet
    Return:
        True if pkt is of allowed type (e.g. non-ARP)
    """
    #-- list test functions
    tests = (_is_arp, _is_ssh, _is_netbios)

    #-- run individual tests
    for t in tests:
        if t(pkt):
            #-- we don't want this paket
            return False

    #-- packet is interesting -- keep it
    return True
