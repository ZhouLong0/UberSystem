import heapq
import numpy as np
import random
import time
from Environment import Environment
from Broker import Broker


class UberSystem:
    def __init__(self, taxis, customers, env):
        """
        drivers: list of drivers
        customers: list of customers
        env: Environment object
        """
        self.__taxis = taxis
        self.__customers = customers
        self.__rides = []
        self.__env = env
        self.__round = 0

        self.__broker = Broker(self.__taxis, self.__env)
        # recommender for 2nd use case
        # TO BE IMPLEMENTED
        # self.__recommender = Recommender(self.__taxis, self.__customers, self.__env)

    def get_customers(self):
        return self.__customers

    def get_rides(self):
        return self.__rides

    def simulate_one_turn_brokering(self, env: Environment):
        """
        Simulate one turn of the Uber system
        Let existing rides move
        Let idle customers request for ride, if a taxi accepts, create a ride and add it to the list of rides
        """
        self.__round += 1
        # move existing rides
        for ride in self.__rides:
            if ride.is_finished():
                self.__rides.remove(ride)
                self.__customers.remove(ride.get_customer())

            ride.move()

            if ride.is_finished():
                self.__rides.remove(ride)
                self.__customers.remove(ride.get_customer())

        # find idle customers, let them request for ride
        idle_customers = [
            customer for customer in self.__customers if customer.is_idle()
        ]

        for customer in idle_customers:
            ride = customer.send_message(self.__broker, "request for ride")
            print("\n")
            if ride is not None:
                self.__rides.append(ride)
        pass

    def simulate_one_turn_recommending(self, env: Environment):
        # TO BE IMPLEMENTED
        ...

    def report_round_count(self):
        return self.__round
    
    def report_num_customers(self):
        return self.__customers

    def report_num_taxis(self):
        return self.__taxis

    def print_state(self):
        print(
            f"-----------------------------Round {self.__round} State of Uber System -----------------------------"
        )
        print("Taxis: ")
        for taxi in self.__taxis:
            print(taxi)
        print("Customers: ")
        for customer in self.__customers:
            print(customer)
        print("Rides: ")
        for ride in self.__rides:
            print(ride)
        print("\n")
