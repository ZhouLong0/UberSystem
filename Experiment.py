from Simulation import Simulation
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Save the data to a JSON file
    num_taxis = 50
    num_customers = 100
    num_samples = 50

    # GENERATION OF TEST CASE
    # Simulation.generate_test_cases(
    #    num_samples, num_customers, num_taxis, constant="None", grid_size=50
    # )

    # Simulation
    sim_rec = Simulation.read_from_file("experiment/test_50_None_constant.json")
    print(sim_rec.customers)
    sim_rec.simulate("Recommender")

    sim_broker = Simulation.read_from_file("experiment/test_50_None_constant.json")
    sim_broker.simulate("Broker")

    # Plot comparison
    fig, ax = plt.subplots()
    ax.plot(sim_rec.get_message_count_per_round(), label="Recommender")
    ax.plot(sim_broker.get_message_count_per_round(), label="Broker")
    ax.text(
        1,
        13,
        f"Customers: {sim_rec.customers} Taxis: {sim_rec.taxis}",
        style="italic",
        bbox={"facecolor": "green", "alpha": 0.5, "pad": 10},
    )

    ax.set_xlabel("Rounds")
    ax.set_ylabel("Message Count")
    ax.set_title(f"Communication between Initiators and Participant")
    ax.legend()

    plt.show()
