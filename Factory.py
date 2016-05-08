import inflect
import sys

from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

class Lone_Item:
    def __hash__(self):
        return hash(self.name)

    def __init__(self, name):
        self.name = name
        self.directory = {}

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]

    def set_desc(self, desc):
        self.desc = desc

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self,other):
        return self.name == other.name

class Item_Count:
    plural_generator = inflect.engine()

    def __init__(self, item, number=1):
        self.number = number
        if isinstance(item, Lone_Item):
            self.item = item
        else:
            raise ValueError("Sent %r to Item_Collection that is not a Lone_Item" % (item))
        self.directory = {}

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]


    def get_item(self):
        return self.item

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def __repr__(self):
        if self.number != 1:
            if self.item.key_in_directory('plural'):
                return str(self.number) + " " + self.item.directory['plural']
            else:
                return str(self.number) + " " + Item_Count.plural_generator.plural(str(self.item))
        else:
            return str(self.item)

    @staticmethod
    def add_ic_to_ic_list(input_list, item_count):
        lone = item_count.get_item()
        for value in input_list:
            if lone == value.get_item():
                value.set_number(item_count.get_number() + value.get_number())
                item_count = -1
                break
        if item_count != -1:
            input_list.append(item_count)
        return input_list

    @staticmethod
    def generate_normalized_items(input_list):
        return_list = []
        for item in input_list:
            if isinstance(item,Lone_Item):
                additem = Item_Count(item, 1)
            elif isinstance(item, Item_Count):
                additem = item
            else:
                raise ValueError\
                    ("Sent %r to Process.generate_normalized_items that is not a Lone_Item or Item_Count" % (item))
            return_list = Item_Count.add_ic_to_ic_list(return_list, additem)
        return return_list

class Item_Collection:
    def __init__(self,input_list = []):
        self.items = Item_Count.generate_normalized_items(input_list)

    def add(self, input_list):
        for item in input_list:
            if isinstance(item,Lone_Item):
                additem = Item_Count(item, 1)
            elif isinstance(item, Item_Count):
                additem = item
            else:
                raise ValueError\
                    ("Sent %r to Item_Collection.add that is not a Lone_Item or Item_Count" % (item))
            self.items = Item_Count.add_ic_to_ic_list(self.items, additem)




class Process:
    def __init__(self,name,input_list = [], output_list = [], time = 1):
        self.name = name
        self.directory = {}
        self.set_inputs(input_list)
        self.set_outputs(output_list)
        self.time = time

    def set_inputs(self, input_list):
        self.inputs = Item_Count.generate_normalized_items(input_list)

    def set_outputs(self, output_list):
        self.inputs = Item_Count.generate_normalized_items(output_list)

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]


class Machine:
    def __init__(self, name = "", process_list = []):
        self.name = name
        self.processes = []
        self.items_contained = []

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]

class Routing:
    def __init__(self,route = [], input = [], output = []):
        self.route = route
        self.input = input
        self.output = output

class Factory:
    def __init__(self):
        self.routings = []
        self.machines = []







Blank_Circuit_Board = Lone_Item("Blank Circuit Board")
Soddered_Circuit_Board = Lone_Item("Soddered Circuit Board")
Loaded_Circuit_Board = Lone_Item("Loaded Circuit Board")
Box_Of_Ten = Item_Count(Blank_Circuit_Board,10)

Sodder_Jet = Process("Sodder Jet",[Blank_Circuit_Board],[Soddered_Circuit_Board])

Sodder_Printer = Machine("",[Sodder_Jet])

print (Box_Of_Ten)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

