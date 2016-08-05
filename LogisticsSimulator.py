import random
import sys
import simpy

from enum import Enum

from LogisticsWindow import LogisticsWindow
from PyQt5.QtWidgets import QApplication

class Design:
    def __init__(self, part_list=[], board_design=[]):
        self.part_list = part_list
        self.board_design = []

    def __repr__(self):
        return ("(" + str(self.part_list) + ", " + str(self.board_design) + ")")


class Quote:
    def __init__(self):
        pass


class Parts:
    def __init__(self, name="GENERIC_", odds=0.1, count=[1]):
        self.odds = odds
        self.count = count
        self.name = name
        self.expected_num_per_design = (sum(self.count)/len(self.count))*(self.odds)


    @staticmethod
    def generate_part(name="GENERIC_"):
        possible_odds = [0.05, 0.1, 0.1, 0.1, 0.2, 0.25, 0.3, 0.5]
        odds = random.choice(possible_odds)
        # Higher the odds, the more likely it should be that there are multiples
        possible_counts = [1]
        for _ in range(0, random.randint(1, 10)):
            count_increment = 0
            for _ in range(0, 10):
                if random.random() < odds:
                    count_increment += 1

            if count_increment != 0:
                possible_counts.append(count_increment)

        return Parts(name=name, odds=odds, count=possible_counts)


class Logistics_Employee:

    class State(Enum):
        waiting = 1
        working_design = 2


    def __init__(self):
        self.status = self.State.waiting

    def run_sim(self,env,world):
        # while True:
        #     print('Start parking at %d' % env.now)
        #     parking_duration = 5
        #     yield env.timeout(parking_duration)
        #     print('Start driving at %d' % env.now)
        #     trip_duration = 2
        #     yield env.timeout(trip_duration)
        while True:
            if self.status == self.State.waiting:
                if world.job_list == []:
                    print("Waiting for job...")
                    yield env.timeout(1)
                else:
                    print(world.job_list)
                    world.job_list = []
                    yield env.timeout(4)






class Board_Manufacturer:
    def __init__(self):
        pass


class Distributor:
#    distributor_list = []

    def __init__(self, name, reliability=1.0, speed=1.0, stock=1.0):
        self.name = name
        self.reliability = reliability
        self.speed = speed
        self.stock_rate = stock
        self.in_stock = []

    def init_stock(self, part_list):
        for entry in part_list:
            num_entry = 0
            for _ in range(0,random.randint(50, 150)):
                if random.random() < entry.odds:
                    num_entry += random.choice(entry.count)
            self.in_stock.append((entry,num_entry))

    def get_name(self):
        return self.name

    def get_stock(self):
        return self.in_stock


class Mail:
    def __init__(self,destination,speed,contents):
        self.timestamp = World.now()
        self.destination = destination
        self.delivered_on = self.timestamp+speed
        self.contents = contents


class Customer:
    def __init__(self):
        pass

    def generate_design(self, part_list):
        design_part_list = []
        for part in part_list:
            if random.random() < part.odds:
                design_part_list.append((part, random.choice(part.count)))
        return Design(design_part_list, [])

class Job:
    def __init__(self):
        pass



class World:
    def __init__(self):
        self.time = 0
        self.distributor_list = []
        self.part_list = []
        self.customer_list = []
        self.job_list = []
        self.environment = simpy.Environment()

    def generate_part(self):
        self.part_list.append(Parts.generate_part("GENERIC_" + str(len(self.part_list))))

    def generate_distributor(self,name):
        distrib = Distributor(name)
        distrib.init_stock(self.part_list)
        self.distributor_list.append(distrib)

    def generate_customer(self,name):
        self.customer_list.append(Customer())

    def generate_design(self,customer=None):
        if customer == None:
            if self.customer_list == []:
                self.generate_customer("Placeholder")
            customer = random.choice(self.customer_list)
        self.job_list = "Meh"
        return customer.generate_design(self.get_part_list())

    def generate_employee(self,employee=None):
        new_employee = Logistics_Employee()
        self.environment.process(new_employee.run_sim(self.environment,self))


    def main_loop(self):
        pass

    def now(self):
        return self.environment.now

    def advance_time(self,timestep):
        self.environment.run(until=(self.environment.now+timestep))

    def get_part_list(self):
        return self.part_list

    def get_stock_list(self):
        return self.distributor_list[0].in_stock

    def get_stock_list_number(self,num):
        return self.distributor_list[num].in_stock

    def get_stock_source_list(self):
        return self.distributor_list


if __name__ == '__main__':

    universe = World()

    for _ in range(0,20):
        universe.generate_part()

    # for _ in range(0,20):
    #     universe.generate_design()

    universe.generate_distributor("megamax")
    universe.generate_distributor("superlock")
    universe.generate_employee()

    app = QApplication(sys.argv)
    ex = LogisticsWindow()

    ex.setWorld(universe)

    sys.exit(app.exec_())