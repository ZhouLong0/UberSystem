from UberSystem import UberSystem
from Taxi import Taxi
from Customer import Customer
from Environment import Environment
import numpy as np


def test1():
    env = Environment(np.zeros((30, 30)))

    driver1 = Taxi(1, (0, 2), 4, env)
    driver2 = Taxi(2, (3, 2), 4, env)
    driver3 = Taxi(3, (2, 0), 4, env)
    driver4 = Taxi(4, (7, 1), 4, env)
    drivers = [driver1, driver2, driver3, driver4]

    customer1 = Customer(1, (0, 3), (3, 3), 1)
    customer2 = Customer(2, (0, 3), (10, 3), 1)
    customer3 = Customer(3, (6, 3), (3, 3), 1)
    customer4 = Customer(4, (6, 3), (10, 3), 1)
    customer5 = Customer(5, (10, 3), (3, 3), 1)
    customers = [customer1, customer2, customer3, customer4, customer5]

    # 30x30 grid
    
    uber_system = UberSystem(drivers, customers, env)

    n_turns = 10
    while uber_system.get_customers():
        uber_system.print_state()

        uber_system.simulate_one_turn_recommending(env)


if __name__ == "__main__":
    test1()
