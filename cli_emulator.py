import cmd
import sys
import getpass
import socket
import platform

version = "0.9"
items = [
    "spam",
    "ham",
    "eggs"
]


class Shell(cmd.Cmd):
    intro = "\n\nTest shell " + version +\
        """\n  by: David Curran (david.curran@ftr.com)\n\
  Type 'help' to see a list of commands\n"""

    prompt = getpass.getuser() + "@" + socket.gethostname() + "_fake$ "
    completekey = 'tab'

    def print_items(self):
        for i in range(0, len(items)):
            print(str(i) + ": " + items[i])

    def print_item(self, index):
        if index is 'last':
            print(str(len(items)-1) + ": " + items[-1])
        else:
            print(str(index) + ": " + items[index])

    def do_list_items(self, args):
        'List items'
        self.print_items()

    def do_create_item(self, args):
        'Create an item: create_item <item>'
        items.append(args)
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
            items[key] = value
            self.print_item(key)
        except IndexError:
            print("Error: Item does not exist")

    def do_read_item(self, args):
        'Read a single item: read_item <index>'
        try:
            self.print_item(int(args))
        except (IndexError, ValueError):
            print("Error: Item does not exist")

    def do_delete_item(self, args):
        'Delete an item: delete_item <index>'
        try:
            del items[int(args)]
            print("OK")
        except IndexError:
            print("Error: Item does not exist")

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
