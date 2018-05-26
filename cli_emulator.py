#!/usr/bin/python3

import cmd
import sys
import getpass
import socket
import platform
import re
from jinja2 import Environment, PackageLoader, select_autoescape

jinja_env = Environment(
    loader=PackageLoader('cli_emulator', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
    )

version = "0.9"

ipadd_pattern = re.compile('\b(?:\d{1,3}\.){3}\d{1,3}\b')

interfaces = {
    "ge-1/0/2": {
        "description": "CKT ETH/12345/A",
        "sub_interfaces": {
            "10": {
                "description": "Bob's Taco Shack Site 1 - CKT VC/123",
                "ip_address": "192.168.2.1/24",
                "type": "Gigabit Ethernet",
                "vlan": 10,
                "proto_state": "up",
                "int_state": "up",
                "bandwidth": "5000M"
            },
            "11": {
                "description": "Bob's Taco Shack Site 2 - CKT VC/124",
                "ip_address": "192.168.3.1/24",
                "type": "Gigabit Ethernet",
                "vlan": 11,
                "proto_state": "up",
                "int_state": "up",
                "bandwidth": "5000M"
            }
        }
    },
    "ge-1/0/1": {
        "description": "CKT ETH/45678/QZ",
        "sub_interfaces": {
            "10": {
                "description": "Bob's Taco Shack Host - CKT VC/125",
                "ip_address": "192.168.1.1/24",
                "type": "Gigabit Ethernet",
                "vlan": 10,
                "proto_state": "down",
                "int_state": "down",
                "bandwidth": "10000M"
            }
        }
    },
    "ge-2/0/0": {
        "description": "Uplink CKT GE/1212345/QZDW",
        "ip_address": "192.168.4.1/24",
        "type": "Ten-Gigabit Ethernet",
        "vlan": 1000,
        "proto_state": "up",
        "int_state": "up",
        "bandwidth": "100000M"
    },
    "loopback0": {
        "description": "BGP Peer Interface",
        "ip_address": "192.168.5.1/32",
        "type": "Loopback",
        "vlan": 0,
        "proto_state": "up",
        "int_state": "up",
        "bandwidth": "100000M"
    }
}

xconnects = {
    "vpn1": {
        "source-int": "ge-1/0/1.10",
        "dest-int": "ge-1/0/2.10",
        "type": "vlan",
    },
    "vpn2": {
        "source-int": "ge-1/0/1.11",
        "dest-int": "ge-1/0/2.10",
        "type": "vlan",
    },
    "offnet-vpn": {
        "source-int": "10.1.1.1",
        "dest-int": "ge-1/0/2.10",
        "type": "mpls"
    }
}

xconnect_hash = {}


class Shell(cmd.Cmd):
    intro = "\n\nTest shell " + version +\
        """\n  by: David Curran (david.curran@ftr.com)\n\
  Type 'help' to see a list of commands\n"""

    prompt = getpass.getuser() + "@" + socket.gethostname() + "_fake$ "
    completekey = 'tab'

    def update_xconnect_hash(self):
        for xconnect in xconnects:
            xconnect_hash[xconnect["source-int"]] = xconnect["dest-int"]
            xconnect_hash[xconnect["dest-int"]] = xconnect["source-int"]

    def check_for_int(self, int):
        if int in interfaces.keys():
            print("True")
            return True

        try:
            int, sub_int = int.split('.')
            if sub_int in interfaces[int]['sub_interfaces'].keys():
                print("True")
                return True
            else:
                print("False")
                return False
        except (ValueError, KeyError):
            print("False")
            return False

    def do_create_xconnect(self, args):
        'create_xconnect <source> <dest> <type>'
        try:
            source, dest, type, name = args.split('\s+')
        except ValueError:
            'create_xconnect <source> <dest> <type> <name>'

        if not self.check_for_int(source) or self.check_for_int(dest):
            if not ipadd_pattern.match(source) or not ipadd_pattern(dest):
                print('source/destination must be valid interface or IP Address')
                return False

        if type not in ['mpls', 'vlan']:
            print('type must be one of [vlan, mpls]')
            return False

        xconnects[name] = {
            "source-int": source,
            "dest-int": dest,
            "type": type
        }

        self.update_xconnect_hash
        print(name)
        return True

    def do_show_xconnects(self, args):
        template = jinja_env.get_template('show-xconnects.tmpl')
        print(template.render(xconnects=xconnects))

        return True


    def do_show_interface(self, args):
        'do_show_interface <interface>.[sub-interface]'

        sub_int = False
        try:
            if '.' in args:
                int, sub_int = args.split('.')
            else:
                int = args
        except ValueError:
            'do_show_interface <interface>[.sub-interface]'

        if int not in interfaces.keys():
            print("Interface {} not found".format(int))
            return False
        if sub_int and sub_int not in interfaces[int]["sub_interfaces"].keys():
            print("Interface {}.{} not found".format(int, sub_int))
            return False

        template = jinja_env.get_template('show_interface.tmpl')
        print(template.render(int=int, sub_int=sub_int, interfaces=interfaces))
        return True

    def do_show_interfaces(self, args):
        'Show all interfaces'
        template = jinja_env.get_template('show_interface.tmpl')

        for int in interfaces:
            print(template.render(int=int, sub_int=False,
                                  interfaces=interfaces))

        return True

    def do_show_device(self, args):
        "Show system info"
        print("Hostname" + socket.gethostname())
        print("OS: " + platform.system())
        print("Release: " + platform.release())
        print("Version: Ubuntu 16.04 LTS")
        print("Machine: " + platform.machine())
        print("Processor: " + platform.processor())

    def do_exit(self, arg):
        print("Goodbye...")
        sys.exit()

    def precmd(self, line):
        line = line.lower()
        return line

    def postcmd(self, stop, line):
        print()


if __name__ == '__main__':
    try:
        Shell().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye...")
        sys.exit()
