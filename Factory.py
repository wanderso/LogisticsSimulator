import inflect
import simpy
import itertools
import sys
import random

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
    def remove_ic_from_ic_list(input_list, item_count):
        lone = item_count.get_item()
        for value in input_list:
            if lone == value.get_item():
                remaining = value.get_number() - item_count.get_number()
                if remaining < 0:
                    raise ValueError\
                        ("Attempted to remove more %r s from list than it contained" % (item_count))
                value.set_number(value.get_number() - item_count.get_number())

                item_count = -1
                break
        if item_count != -1:
            raise ValueError\
                ("Attempted to remove %r from list that did not contain it" % (item_count))
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
                additem = Item_Count(item.get_item(), item.get_number())
            else:
                raise ValueError\
                    ("Sent %r to Item_Collection.add that is not a Lone_Item or Item_Count" % (item))
            self.items = Item_Count.add_ic_to_ic_list(self.items, additem)

    def remove(self, remove_list):
        for item in remove_list:
            if isinstance(item, Lone_Item):
                removeitem = Item_Count(item, 1)
            elif isinstance(item, Item_Count):
                removeitem = item
            else:
                raise ValueError\
                    ("Sent %r to Item_Collection.add that is not a Lone_Item or Item_Count" % (item))
            self.items = Item_Count.remove_ic_from_ic_list(self.items, removeitem)

    def contents(self):
        return self.items

    def count_specific_item(self,item):
        if isinstance(item, Lone_Item):
            for object in self.items:
                if (object.get_item() == item):
                    return object.get_number()
            return 0
        elif isinstance(item, Item_Count):
            for object in self.items:
                if (object.get_item() == item.get_item()):
                    return object.get_number()
            return 0

    def __contains__(self,item):
        if isinstance(item, Lone_Item):
            for object in self.items:
                if(object.get_item() == item):
                    return True
            return False
        elif isinstance(item, Item_Count):
            for object in self.items:
                if (object.get_item() == item.get_item()):
                    return object.get_number() >= item.get_number()
            return False

    def __str__(self):
        return self.items.__str__()


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

    def __len__(self):
        return len(self.route)


class Factory:
    def __init__(self):
        self.routings = []
        self.machines = []
        self.widgets = []
        self.customers = []
        self.orders = []
        self.environment = simpy.Environment()
        self.items = Item_Collection()
        self.widget_count = 0
        random.seed()

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

        self.items.remove(input)
        make_object = Widget(routing, id=self.widget_count)
        self.widget_count += 1
        self.widgets.append(make_object)

    def add_customer(self, odds=0.1):
        env = self.get_environment()
        new_cust = Customer(env, odds=odds)
        self.customers.append(new_cust)
        env.process(new_cust.run())

    def logic(self):
        self.logic_traditional_factory()

    def logic_tempo_factory(self):
        add_orders = []
        for customer in self.customers:
            if customer.get_order_dirty():
                for entry in customer.get_orders():
                    add_orders.append(entry)
        print add_orders


    def logic_traditional_factory(self):
        for routing in self.routings:
            input_collected = True
            input_max = -1
            for item in routing.input:
                if item not in self.items:
                    input_collected = False
                else:
                    total_input = item.get_number()
                    total_output = self.items.count_specific_item(item.get_item())
                    items_available = int(total_output/total_input)
                    if input_max == -1:
                        input_max = items_available
                    elif input_max > items_available:
                        input_max = items_available

            if input_collected:
                for i in range(0,input_max):
                    self.engage_routing(routing)

    def process_widgets(self):
        env = self.get_environment()
        remove_widgets = []
        for widget in self.widgets:
            if widget.is_finished():
                remove_widgets.append(widget)
            elif not widget.is_running():
                proc = widget.get_proc()
                for machine in self.machines:
                    if machine.contains_process(proc):
                        env.process(widget.send_widget_to_machine(machine, proc, env))
                        continue
        for widget in remove_widgets:
            self.widgets.remove(widget)
            self.items.add(widget.get_output())





    def run(self, timestamp):
        print (self.items)
        env = self.get_environment()
        for i in range(env.now+1,timestamp):
            self.logic()
            self.process_widgets()
            env.run(until=i)
        print (self.items)


    def get_environment(self):
        return self.environment

class Customer:
    def __init__(self, env, odds=0.1):
        self.environment = env
        self.odds = odds
        self.running = True
        self.order_dirty = False
        self.orders = []

#    def run(self):
#        if random.random() < self.odds:
#            print "Generate order"

    def generate_order(self):
        new_order = Order(self)
        self.orders.append(new_order)
        self.order_dirty = True

    def get_orders(self):
        return_list = []
        for entry in self.orders:
            return_list.append(entry)
        self.orders = []
        self.order_dirty = False
        return return_list

    def get_order_dirty(self):
        return self.order_dirty

    def run(self):
        env = self.environment
        time = 10
        while self.running:
            time = 1
            while random.random() < self.odds:
                time += 1
            self.generate_order()
            yield env.timeout(env.now + time)


class Order:
    def __init__(self,customer):
        self.customer = customer

class Widget:
    def __init__(self, routing, id = 0):
        self.routing = routing
        self.pointer = 0
        self.running = False
        self.finished = False
        self.id = id
        self.item_contents = Item_Collection()
        self.item_contents.add(routing.get_input())

    def is_running(self):
        return self.running

    def is_finished(self):
        return self.finished

    def get_output(self):
        return self.routing.get_output()

    def get_proc(self):
        return self.routing[self.pointer]

    def send_widget_to_machine(self,machine,proc,env):
        self.running = True
        with machine.get_resource().request() as req:
            yield req
            print ("Undergoing machine process %s for widget %s at time %d" % (str(proc), str(self.id), env.now))
            yield env.timeout(proc.get_time())
            print ("Finished machine process %s for widget %s at time %d" % (str(proc), str(self.id), env.now))
            self.pointer += 1
            self.item_contents = proc
        if self.pointer == len(self.routing):
            self.finished = True
        else:
            self.running = False



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
Buy_Boards = Process("Buy More Boards", list(itertools.repeat(Loaded_Circuit_Board, 10)),list(itertools.repeat(Blank_Circuit_Board, 15)),time=10)

Solder_Printer = Machine("Solder Printer",[Solder_Jet])
Worker = Machine("Worker",[Buy_Boards])
Driver = Machine("Pick and Place Machine", [Driver_Load])

#Board_Construct_1 = Routing(route=[Solder_Jet,Hand_Load], input=[Blank_Circuit_Board],output=[Loaded_Circuit_Board])
Board_Construct_2 = Routing(route=[Solder_Jet,Driver_Load], input=[Blank_Circuit_Board],output=[Loaded_Circuit_Board])


Buy_More_Boards = Routing(route=[Buy_Boards], input=list(itertools.repeat(Loaded_Circuit_Board, 10)),output=list(itertools.repeat(Blank_Circuit_Board, 15)))



Tempo_Automation.add_machine(Solder_Printer)
Tempo_Automation.add_machine(Worker)
Tempo_Automation.add_machine(Driver)

#Tempo_Automation.add_routing(Board_Construct_1)
Tempo_Automation.add_routing(Board_Construct_2)
Tempo_Automation.add_routing(Buy_More_Boards)

Tempo_Automation.add_customer()
Tempo_Automation.add_customer()


#env = Tempo_Automation.get_environment()

#env.process(Widget_1.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))
#env.process(Widget_2.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))
#env.process(Widget_3.send_widget_to_machine(Solder_Printer,Tempo_Automation.get_environment()))

#Tempo_Automation.logic()

Tempo_Automation.run(302)

print ("Orders: %s" % str(Tempo_Automation.customers[0].orders))

#env.run(until=10)

#print (Box_Of_Ten)