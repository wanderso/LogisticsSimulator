import inflect
import simpy
import sys

#from MainWindow import MainWindow
#from PyQt5.QtWidgets import QApplication

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

    def __str__(self):
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

    def __iter__(self):
        return self.items.__iter__()

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

    def contents(self):
        return self.items

    def __contains__(self,item):
        if isinstance(item, Lone_Item):
            for object in self.items:
                if(object.get_item() == item):
                    return True
            return False
        elif isinstance(item, Item_Count):
            return False




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
        self.outputs = Item_Count.generate_normalized_items(output_list)

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]

    def get_time(self):
        return self.time

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs


    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def run_process(self, env):
        pass


class Machine:
    def __init__(self, name = "", process_list = []):
        self.name = name
        self.processes = process_list
        self.items_contained = []
        self.idle = True
        self.environment = False
        self.res = False

    def add_to_directory(self, key, value):
        self.directory[key] = value

    def key_in_directory(self, key):
        return key in self.directory

    def get_from_directory(self, key):
        return self.directory[key]

    def contains_process(self, process):
        for entry in self.processes:
            if entry == process:
                return entry
        return False

    def is_free(self):
        return self.idle

    def run_process(self,process):
        while self.environment:
            yield(process.get_time())

        yield False

    def set_environment(self,environment):
        self.environment = environment
        self.res = simpy.Resource(self.environment, capacity=2)

    def get_resource(self):
        return self.res


    def __str__(self):
        return self.name



class Routing:
    def __init__(self,route = [], input = [], output = []):
        self.route = route
        self.input = Item_Collection(input)
        self.output = Item_Collection(output)

    def get_route(self):
        return self.route

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def __getitem__(self, item):
        return self.route[item]


class Factory:
    def __init__(self):
        self.routings = []
        self.machines = []
        self.environment = simpy.Environment()
        self.items = Item_Collection()

    def add_items(self, item_list):
        self.items.add(item_list)

    def add_routing(self,routing):
        self.routings.append(routing)

    def add_machine(self,machine):
        machine.set_environment(self.environment)
        self.machines.append(machine)

    def engage_routing(self, routing):
        route = routing.get_route()
        input = routing.get_input()
        output = routing.get_output()

#        for machine in self.machines:
#            if not machine.is_free():
#                continue
#            proc = machine.contains_process(route[0])
#            if not proc:
#                continue
#            print(proc)


    def logic(self):
        items_available = []
        for item_count in self.items.contents():
            items_available.append(item_count.get_item())


        for routing in self.routings:
            for item in routing.input:
                if item.get_item() in items_available:
                    print (item)



    def run(self, timestamp):
#        print(self.items)
        self.environment.run(until=timestamp)

    def get_environment(self):
        return self.environment



class Widget:
    def __init__(self, routing):
        self.routing = routing
        self.pointer = 0

    def send_widget_to_machine(self,machine,env):
        proc = machine.contains_process(self.routing[self.pointer])
        with machine.get_resource().request() as req:
            yield req
            #print (proc.get_inputs())
            #print ("Undergoing machine process at time %d" % env.now)
            yield env.timeout(proc.get_time())
            #print ("Finished machine process at time %d" % env.now)
            #print (proc.get_outputs())


    def increment_ptr(self):
        self.pointer += 1





Blank_Circuit_Board = Lone_Item("Blank Circuit Board")
Soldered_Circuit_Board = Lone_Item("Soldered Circuit Board")
Loaded_Circuit_Board = Lone_Item("Loaded Circuit Board")
Box_Of_Ten = Item_Count(Blank_Circuit_Board,10)

Tempo_Automation = Factory()

Tempo_Automation.add_items([Box_Of_Ten])

Solder_Jet = Process("Solder Jet",[Blank_Circuit_Board],[Soldered_Circuit_Board], time=2)
#Hand_Load = Process("Hand Load Circuit Board",[Soldered_Circuit_Board],[Loaded_Circuit_Board], time=3)
Driver_Load = Process("Machine Load Circuit Board",[Soldered_Circuit_Board],[Loaded_Circuit_Board], time=1)

Solder_Printer = Machine("Solder Printer",[Solder_Jet])
#Worker = Machine("Worker",[Hand_Load])
Driver = Machine("Pick and Place Machine", [Driver_Load])

#Board_Construct_1 = Routing(route=[Solder_Jet,Hand_Load], input=[Blank_Circuit_Board],output=[Loaded_Circuit_Board])
Board_Construct_2 = Routing(route=[Solder_Jet,Driver_Load], input=[Blank_Circuit_Board],output=[Loaded_Circuit_Board])

Widget_1 = Widget(Board_Construct_2)
Widget_2 = Widget(Board_Construct_2)
Widget_3 = Widget(Board_Construct_2)
Widget_4 = Widget(Board_Construct_2)
Widget_5 = Widget(Board_Construct_2)


Tempo_Automation.add_machine(Solder_Printer)
#Tempo_Automation.add_machine(Worker)
Tempo_Automation.add_machine(Driver)

#Tempo_Automation.add_routing(Board_Construct_1)
Tempo_Automation.add_routing(Board_Construct_2)

#env = Tempo_Automation.get_environment()

#env.process(Widget_1.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))
#env.process(Widget_2.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))
#env.process(Widget_3.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))

Tempo_Automation.logic()

Tempo_Automation.run(10)
#env.run(until=10)

#print (Box_Of_Ten)