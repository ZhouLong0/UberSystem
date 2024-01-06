import json
import random
import numpy as np
import sys
import io
import os
import matplotlib.pyplot as plt

from Taxi import Taxi
from Customer import Customer
from Environment import Environment
from UberSystem import UberSystem

class Simulation:
    def __init__(self, env, customers, taxis):
        self.env = env
        self.customers = len(customers)
        self.taxis = len(taxis)
        self.uber_system = UberSystem(taxis, customers, self.env)
        self.message_count_per_round = []
        
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
                    with open(os.path.join("test_cases", f"Customers_{i}_{constant}_constant.json"), "w") as f:
                        json.dump([data], f, indent=4)
            else:
                for i in range(1, num_samples+1):
                    data = Simulation.generate_environment_data(num_taxis, i, grid_size)
                    with open(os.path.join("test_cases", f"Customers_{i}_{constant}_constant.json"), "w") as f:
                        json.dump([data], f, indent=4)
            
        #Increment number of Taxis
        if constant == 'Customers':
            if num_samples >= num_taxis:
                for i in range(1, num_taxis+1):
                    data = Simulation.generate_environment_data(i, num_customers, grid_size)
                    with open(os.path.join("test_cases",f"Taxis_{i}_{constant}_constant.json"), "w") as f:
                        json.dump([data], f, indent=4)
            else:
                for i in range(1, num_samples+1):
                    data = Simulation.generate_environment_data(i, num_customers, grid_size)
                    with open(os.path.join("test_cases",f"Taxis_{i}_{constant}_constant.json"), "w") as f:
                        json.dump([data], f, indent=4)


        if constant == 'None':
            for i in range(1, num_samples+1):
                data = Simulation.generate_environment_data(num_taxis, num_customers, grid_size)
                with open(os.path.join("test_cases", f"test_{i}_{constant}_constant.json"), "w") as f:
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
            grid = np.array(simulation["Environment"])
            env = Environment(grid)
            
            for customer in CustomerList:
                customers.append(Customer(customer["Customer"], tuple(customer["start_pos"][0]), tuple(customer["dest_pos"][0]), customer["seat_n"]))
            for taxi in TaxiList:
                taxis.append(Taxi(taxi["Taxi"], tuple(taxi["start_pos"][0]), taxi["n_seats"], env))
            
        return Simulation(env, customers, taxis)
    
    def simulate(self, case):
        self.message_count_per_round = []
        if(case == 'Broker'):
            number_of_messages = []
            logs = []
            while(self.uber_system.get_customers()):
                
                original_stdout = sys.stdout
                sys.stdout = io.StringIO()
    
                #self.env.print_state()
                self.uber_system.simulate_one_turn_brokering(self.env)
                sys.stdout.seek(0)
                message_list = sys.stdout.read().splitlines()
                number_of_messages.append(len(message_list))

                logs.append(message_list)
                self.message_count_per_round.append(len(message_list))

                sys.stdout = original_stdout
                print(f"Number of Messages for Round {self.uber_system.report_round_count()}: {len(message_list)}")
                
            empty_logs_count = sum(1 for log in logs if not log)

            with open(os.path.join("logs", f"Logs_Broker.json"), "w") as json_file:
                json.dump({"logs": logs}, json_file, indent=4)
                
        if (case == 'Recommender'):
            number_of_messages = []
            logs = []
            while(self.uber_system.get_customers()):
                
                original_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                self.uber_system.simulate_one_turn_recommending(self.env)
                sys.stdout.seek(0)
                message_list = sys.stdout.read().splitlines()
                number_of_messages.append(len(message_list))

                logs.append(message_list)
                self.message_count_per_round.append(len(message_list))
        
                sys.stdout = original_stdout
                print(f"Number of Messages for Round {self.uber_system.report_round_count()}: {len(message_list)}")
            
            empty_logs_count = sum(1 for log in logs if not log)

            with open(os.path.join("logs", f"Logs_Recommender.json"), "w") as json_file:
                json.dump({"logs": logs}, json_file, indent=4)

    def get_message_count_per_round(self):
        return self.message_count_per_round  



# Save the data to a JSON file
num_taxis = 5
num_customers = 10
num_samples = 8
Simulation.generate_test_cases(num_samples, num_customers, num_taxis, constant='Customers', grid_size=10)

#Simulation
sim_rec = Simulation.read_from_file('test_cases/Taxis_5_Customers_constant.json')
sim_rec.simulate('Recommender')

sim_broker = Simulation.read_from_file('test_cases/Taxis_5_Customers_constant.json')
sim_broker.simulate('Broker')

#Plot comparison
fig, ax = plt.subplots()
ax.plot(sim_rec.get_message_count_per_round(), label='Recommender')
ax.plot(sim_broker.get_message_count_per_round(), label='Broker')
ax.text(1, 13, f'Customers: {sim_rec.customers} Taxis: {sim_rec.taxis}', style='italic', bbox={
        'facecolor': 'green', 'alpha': 0.5, 'pad': 10})

ax.set_xlabel('Rounds')
ax.set_ylabel('Message Count')
ax.set_title(f'Communication between Initiators and Participant')
ax.legend()

plt.show()

#todo: make the grid with obstacles
