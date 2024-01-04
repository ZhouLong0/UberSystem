import json
import random
import numpy as np
import sys
import io
from Taxi import Taxi
from Customer import Customer
from Environment import Environment
from UberSystem import UberSystem

class Simulation:
    def __init__(self, grid, customers, taxis):
        self.env = Environment(grid)
        self.uber_system = UberSystem(taxis, customers, self.env)
        #self.num_taxis = self.uber_system.report_num_taxis()
        #self.num_customers = self.uber_system.report_num_customers()
        
    def generate_environment_data(num_taxis, num_customers, grid_size):

        # Generate the environment matrix with 0 values
        environment = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Randomly place taxis and customers in the matrix, avoiding collisions
        available_positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]
        taxi_positions = random.sample(available_positions, num_taxis)
        available_positions = [pos for pos in available_positions if pos not in taxi_positions]
        customer_positions_start = random.sample(available_positions, num_customers)
        available_positions = [pos for pos in available_positions if pos not in customer_positions_start]
        customer_positions_des = random.sample(available_positions, num_customers)
        
        
        data = {
        "Customers": [
            {"Customer": i+1, "start_pos": [list(start_pos)], "dest_pos": [list(des_pos)], "seat_n": 1}
            for i, (start_pos, des_pos) in enumerate(zip(customer_positions_start, customer_positions_des))
        ],
        "Taxis": [
            {"Taxi": i + 1, "start_pos": [list(pos)], "n_seats": 4}
            for i, pos in enumerate(taxi_positions)
        ],
        "Environment": environment
        }

        return data

    def generate_test_cases(num_samples, num_customers, num_taxis, constant='None', grid_size=10):
        #Increment number of Customers
        if constant == 'Taxis':
            if num_samples >= num_customers:
                for i in range(1, num_customers+1):
                    data = Simulation.generate_environment_data(num_taxis, i, grid_size)
                    with open(f"Customers_{i}_{constant}_constant.json", "w") as f:
                        json.dump([data], f, indent=4)
            else:
                for i in range(1, num_samples+1):
                    data = Simulation.generate_environment_data(num_taxis, i, grid_size)
                    with open(f"Customers_{i}_{constant}_constant.json", "w") as f:
                        json.dump([data], f, indent=4)
            
        #Increment number of Taxis
        if constant == 'Customers':
            if num_samples >= num_taxis:
                for i in range(1, num_taxis+1):
                    data = Simulation.generate_environment_data(i, num_customers, grid_size)
                    with open(f"Taxis_{i}_{constant}_constant.json", "w") as f:
                        json.dump([data], f, indent=4)
            else:
                for i in range(1, num_samples+1):
                    data = Simulation.generate_environment_data(i, num_customers, grid_size)
                    with open(f"Taxis_{i}_{constant}_constant.json", "w") as f:
                        json.dump([data], f, indent=4)


        if constant == 'None':
            for i in range(1, num_samples+1):
                data = Simulation.generate_environment_data(num_taxis, num_customers, grid_size)
                with open(f"test_{i}_{constant}_constant.json", "w") as f:
                    json.dump([data], f, indent=4)

    @staticmethod
    def read_from_file(filepath):
        customers = []
        taxis = []
        with open(filepath, 'r') as file:
            try:
                simulations = json.load(file)
            except:
                raise Exception ("File is not JSON")
            
        for simulation in simulations:
            CustomerList = simulation["Customers"]
            TaxiList = simulation["Taxis"]
            for customer in CustomerList:
                customers.append(Customer(customer["Customer"], tuple(customer["start_pos"][0]), tuple(customer["dest_pos"][0]), customer["seat_n"]))
            for taxi in TaxiList:
                taxis.append(Taxi(taxi["Taxi"], tuple(taxi["start_pos"][0]), taxi["n_seats"]))
            grid = np.array(simulation["Environment"])
        return Simulation(grid, customers, taxis)
    
    def simulate(self):
        number_of_messages = []
        logs = []
        while(self.uber_system.get_customers()):
            
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()
  
            #self.uber_system.print_state()
            self.uber_system.simulate_one_turn_brokering(self.env)
            sys.stdout.seek(0)
            message_list = sys.stdout.read().splitlines()
            number_of_messages.append(len(message_list))

            logs.append(message_list)
    
            sys.stdout = original_stdout
            #print(f"Number of Messages for Round {self.uber_system.report_round_count()}: {len(message_list)}")
            
        empty_logs_count = sum(1 for log in logs if not log)

        with open(f"Logs.json", "w") as json_file:
            json.dump({"logs": logs}, json_file, indent=4)

# Save the data to a JSON file
num_taxis = 25
num_customers = 3
num_samples = 20
Simulation.generate_test_cases(num_samples, num_customers, num_taxis, constant='Customers', grid_size=10)


sim = Simulation.read_from_file('Taxis_1_Customers_constant.json')
sim.simulate()

#todo: make the grid with obstacles
