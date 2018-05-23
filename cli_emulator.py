#!/usr/local/bin/python3

import cmd
import sys
import getpass
import socket
import platform

version = "0.9"
items = [
    {
        "name": "spam",
        "resources": ["resource 1"]
    },
    {
        "name": "ham",
        "resources": ["resource 1"]
    },
    {
        "name": "eggs",
        "resources": ["resource 1"]
    }
]


class Shell(cmd.Cmd):
    intro = "\n\nTest shell " + version +\
        """\n  by: David Curran (david.curran@ftr.com)\n\
  Type 'help' to see a list of commands\n"""

    prompt = getpass.getuser() + "@" + socket.gethostname() + "_fake$ "
    completekey = 'tab'

    def print_items(self):
        for i in range(0, len(items)):
            print(str(i) + ": " + items[i]['name'])

    def print_item(self, index):
        if index is 'last':
            print(str(len(items)-1) + ": " + items[-1]['name'])
        else:
            print(str(index) + ": " + items[index]['name'])

    def print_resources(self, item):
        if len(items[item]['resources']) is 0:
            print("Error: Item has no resources")
            return
        for i, resource in enumerate(items[item]["resources"]):
            print("  " + str(i) + ": " + resource)

    def print_resource(self, item, resource):
        print("  " + str(item) + ": " + items[item]["resources"][resource])


    def do_list_items(self, args):
        'List items'
        self.print_items()

    def do_create_item(self, args):
        'Create an item: create_item <item>'
        item = {
            "name": args.strip(' \t\r\n'),
            "resources": []
        }
        items.append(item)
        self.print_item('last')

    def do_update_item(self, args):
        'Update item: update_item <index>:<item> (e.g. \'3:spam\' )'
        try:
            key, value = args.split(':')
            key = int(key)
        except (TypeError, ValueError):
            print("""Error: Enter item in the format:
                  \n  <item number>:<item>\n  e.g. 3:spam""")
            return False

        try:
            items[key] = value.strip(' \t\r\n')
            self.print_item(key)
        except IndexError:
            print("Error: Item does not exist")

    def do_read_item(self, args):
        'Read a single item: read_item <index>'
        try:
            self.print_item(int(args))
            self.print_resources(int(args))

        except (IndexError, ValueError):
            print("Error: Item does not exist")

    def do_delete_item(self, args):
        'Delete an item: delete_item <index>'
        try:
            del items[int(args)]
            print("OK")
        except IndexError:
            print("Error: Item does not exist")

    def do_create_resource(self, args):
        'Create a resource: create_resource <item index>: <resource>\n (e.g. 3: resource1)'
        try:
            item, new_resource = args.split(':')
            items[int(item)]['resources'].append(new_resource.strip(' \t\r\n'))
            print("OK")
        except IndexError:
            print("Error: Item does not exist")
        except (ValueError, TypeError):
            print ('Create a resource: create_resource <item index>: <resource>\n (e.g. 3: resource1)')


    def do_read_resource(self, args):
        'Read a resource: read_resource <item index>:<resource index>\n (e.g. 3:2)'
        try:
            item, resource = args.split(':')
            print("OK")
            self.print_resource(int(item), int(resource))
        except IndexError:
            print("Error: Item does not exist")
        except (ValueError, TypeError):
            print ('Create a resource: create_resource <item index>: <resource>\n (e.g. 3: resource1)')


    def do_update_resource(self, args):
        'Update a resource: update_resource <item index>:<resource index>:<resource>\n (e.g. 3:2:bob)'
        try:
            item, resource, update = args.split(':')
            items[int(item)]['resources'][int(resource)] = update.strip(' \t\r\n')
            print("OK")
            self.print_resource(int(item), int(resource))
        except IndexError:
            print("Error: Item or resource does not exist")
        except (ValueError, TypeError):
            print ('Update a resource: update_resource <item index>:<resource index>:<resource>\n (e.g. 3:2:bob)')


    def do_delete_resource(self, args):
        'Delte a resource: delete_resource <item index>:<resource index>\n (e.g. 3:2)'
        try:
            item, resource = args.split(':')
            del items[int(item)]['resources'][int(resource)]
            print("OK")
        except IndexError:
            print("Error: Item or resource does not exist")
        except (ValueError, TypeError):
            print ('Delete a resource: delete_resource <item index>:<resource index>\n (e.g. 3:2)')

    def do_list_resources(self, args):
        'List resources: list_resources <item index>'
        try:
            self.print_resources(int(args))
        except IndexError:
            print("Error: Item does not exist")
        except (ValueError, TypeError):
            print ('Create a resource: create_resource <item index>: <resource>\n (e.g. 3: resource1)')


    def do_show_device(self, args):
        "Show system info"
        print("OS: " + platform.system())
        print("Release: " + platform.release())
        print("Version: " + platform.version())
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
