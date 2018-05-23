A simple CLI emulator to use when playing with Blue Planet. It has all of the CRUDL functions and a "show device" type function. Requires Python 3.

```
currand@M_C02N72W0G3QK_fake$ help

Documented commands (type help <topic>):
========================================
help

Undocumented commands:
======================
create_item  delete_item  exit  list_items  read_item  show_device  update_item

currand@M_C02N72W0G3QK_fake$ exit
Goodbye...
currand@M_C02N72W0G3QK ~/code/cli_emulator $ atom Readme.md
currand@M_C02N72W0G3QK ~/code/cli_emulator $ python cli_emulator.py
Test shell
currand@M_C02N72W0G3QK_fake$ help

Documented commands (type help <topic>):
========================================
help

Undocumented commands:
======================
create_item  delete_item  exit  list_items  read_item  show_device  update_item

currand@M_C02N72W0G3QK_fake$ list_items
0: spam
1: ham
2: eggs
currand@M_C02N72W0G3QK_fake$ read_item 2
2:eggs
currand@M_C02N72W0G3QK_fake$ show_device
OS: Darwin
Release: 16.7.0
Version: Darwin Kernel Version 16.7.0: Mon Nov 13 21:56:25 PST 2017; root:xnu-3789.72.11~1/RELEASE_X86_64
Machine: x86_64
Processori386
currand@M_C02N72W0G3QK_fake$
```
