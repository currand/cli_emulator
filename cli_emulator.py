import future
import cmd
import sys
import getpass
import socket
import shlex
import platform

items = [
    "spam",
    "ham",
    "eggs"
]

port = 8123

class Shell(cmd.Cmd):
    intro = "Test shell"
    prompt = getpass.getuser() + "@" + socket.gethostname() + "_fake$ "

    def print_items(self):
        for i in range(0, len(items)):
            print(str(i) + ": " + items[i])

    def do_list_items(self, args):
        self.print_items()

    def do_create_item(self, args):
        items.append(args)
        self.print_items()

    def do_update_item(self, args):
        try:
            key, value = args.split(':')
            key = int(key)
        except (TypeError, ValueError):
            print("Enter item in the format:\n  <item number>:<item>\n  e.g. 3:spam")
            return False

        try:
            items[key] = value
            print(str(key) + ":" + value)
        except IndexError:
            print("Item does not exist")

    def do_read_item(self, args):
        try:
            print(args + ":" + items[int(args)])
        except (IndexError, ValueError):
            print("Item does not exist")

    def do_delete_item(self, args):
        try:
            del items[int(args)]
        except IndexError:
            print("Item does not exist")

    def do_show_device(self, args):
        print("OS: " + platform.system())
        print("Release: " + platform.release())
        print("Version: " + platform.version())
        print("Machine: " + platform.machine())
        print("Processor" + platform.processor())


    def do_exit(self, arg):
        print("Goodbye...")
        sys.exit()


if __name__ == '__main__':
    Shell().cmdloop()
