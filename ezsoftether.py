#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Softether Automation Script
Dev: K4YT3X
Date Created: May 25, 2018
Last Modified: July 8, 2018

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018 K4YT3X
"""
from Avalon.framework import Avalon
import argparse
import configparser
import os
import socket
import subprocess

VERSION = '1.0.0'


def process_arguments():
    """ This function parses all command line arguments """
    parser = argparse.ArgumentParser()
    control_group = parser.add_argument_group('Controls')
    control_group.add_argument('-s', '--start', help='Start VPN client and route traffic', action='store_true', default=False)
    control_group.add_argument('-r', '--stop', help='Stop VPN client and restore original connection', action='store_true', default=False)
    control_group.add_argument('-i', '--interface', help='Specify the vpn interface', action='store', default=False)
    control_group.add_argument('-g', '--gateway', help='Specify remote gateway (server) address', action='store', default=False)
    control_group.add_argument('-v', '--version', help='Print software version and legal information', action='store_true', default=False)
    return parser.parse_args()


def shell_execute(command):
    """
    Print the command to be executed
    by shell and execute the command
    """
    Avalon.dbgInfo('Executing: {}'.format(command))
    os.system(command)


def get_gateway_ip():
    """ Get default gateway IP

    Get the default gateway IP address by
    inspecting the routing tables.

    Returns:
        str -- IP address of default gateway
    """
    Avalon.info('Getting gateway IP address')
    raw = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE)
    output = raw.communicate()[0].decode().split('\n')
    for line in output:
        if line.split(' ')[0] == 'default' and 'wlan0' in line:
            Avalon.dbgInfo('Got gateway IP: {}'.format(line.split(' ')[2]))
            return line.split(' ')[2]


def get_original_route():
    """ Record pre-routing routes

    This function gets the original routing
    table for restoration.

    Returns:
        str -- the original routing statement
    """
    Avalon.info('Getting original routing information')
    raw = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE)
    output = raw.communicate()[0].decode().split('\n')
    Avalon.dbgInfo('Route: {}'.format(output[0]))
    return output[0]


def resolve_dns(domain):
    """ Resolve IP address of a domain name"""
    return socket.gethostbyname_ex(domain)[2][0]


def route():
    """ Route the internet through VPN

    Route the internet through the virtual
    softether vpn interface. This function
    will write the computer routing table
    using "ip route" command
    """
    rhost = resolve_dns(args.gateway)
    original_route = get_original_route()
    gateway_ip = get_gateway_ip()

    softether = configparser.ConfigParser()
    softether['SE'] = {}
    softether['SE']['ORIGINAL'] = original_route
    softether['SE']['RHOST'] = rhost
    with open('/tmp/original_route.tmp', 'w') as softetherf:
            softether.write(softetherf)

    shell_execute('ip route add {} via {} dev wlan0 proto static'.format(rhost, gateway_ip))
    shell_execute('dhclient {}'.format(args.interface))
    shell_execute('ip route del default')


def restore_route():
    """ Restore routing table

    Restore the system routing table to
    how it was before vpn was routed through
    the virtual vpn interface.
    """
    Avalon.info('Restoring original network connection')
    softether = configparser.ConfigParser()
    softether.read('/tmp/original_route.tmp')
    original_route = softether['SE']['ORIGINAL']
    rhost = softether['SE']['RHOST']

    shell_execute('dhclient -r {}'.format(args.interface))
    shell_execute('vpnclient stop')
    shell_execute('ip route del default')
    shell_execute('ip route del {}'.format(rhost))
    shell_execute('ip route add {}'.format(original_route))


# /////////////////// Execution /////////////////// #

args = process_arguments()

if args.version:  # prints program legal / dev / version info
    print("Current Version: " + VERSION)
    print("Author: K4YT3X")
    print("License: GNU GPL v3")
    print("Github Page: https://github.com/K4YT3X/EZSoftether")
    print("Contact: narexium@gmail.com")
    print()
    exit(0)

if os.getuid() != 0:
    Avalon.error('This script must be run as root\n')
    exit(1)

if not args.interface or not args.gateway:
    Avalon.error('VPN interface and gateway address must be provided\n')
    exit(1)
if not args.start and not args.stop:
    Avalon.error('No operation specified (start / stop)\n')
    exit(1)

try:
    if args.start:
        shell_execute('vpnclient start')
        while True:
            try:
                # Check if vpn interface is up and running
                if os.path.isdir('/sys/class/net/{}'.format(args.interface)):
                    break
            except FileNotFoundError:  # if interface not present
                pass
        route()
    elif args.stop:
        restore_route()
except IndexError:
    Avalon.warning('No operation specified')
    exit(0)
