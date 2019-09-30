#!python3
"""
Common subroutines for the streaming packet dissector
"""

#import sys, os
import scapy.all as scapy

def _is_t38(pkt):
    """
    Test if a packet encapsulates T38 Fax protocol.

    Input:
        pkt -- scapy packet
    Return:
        True for T38, False otherwise
    """
    #-- first, we need only UDP (0x11) packets
    if (pkt.haslayer("UDP") and pkt.haslayer("Raw")):
        r = pkt["Raw"].load. \
                decode("ascii", errors = "backslashreplace").split("\r\n")
        if any("T38" in s for s in r):
            return True

    return False


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
    if pkt.haslayer("TCP"):
        p = pkt["TCP"]
    elif pkt.haslayer("UDP"):
        p = pkt["UDP"]
    else:
        return False

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
    if pkt.haslayer("TCP"):
        t = pkt["TCP"]
        if ((t.sport == 22) or (t.dport == 22)):
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
