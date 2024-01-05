from Ride import Ride
from Taxi import Taxi
from Customer import Customer


class Broker:
    def __init__(self, taxis: list[Taxi], env):
        """
        taxis: list of Taxi objects
        env: Environment object
        """
        self.__taxis = taxis
        self.__env = env
        self.__message_sent = 0
        self.__message_received = 0

    def receive_message(self, customer: Customer, message: str):
        """
        The broker receive request for taxi message from a customer
        parameters:
            customer: Customer object
            message: string
        returns:
            Ride object if a taxi accepted the request
            None otherwise
        """
        print(f"Recommender received message {message} from {customer}")
        self.__message_received += 1
        if message == "request for ride":
            ride = self.__request_for_ride(customer)
            return ride
        # find taxi with enough seats
        return None

    def __request_for_ride(self, customer: Customer):
        """
        parameters:
            customer: Customer object

        forwards request for ride to taxis with enough seats from the nearest to furthest, don't know if they accept or not (free or not)
        returns:
            Ride object if a taxi accepted the request
            None otherwise
        """
        enough_seats_taxis = [
            taxi
            for taxi in self.__taxis
            if taxi.get_seats() >= customer.get_req_seats()
        ]

        if len(enough_seats_taxis) == 0:
            print(f"no taxi with enough seats for {customer}")
            customer.ride_rejected()
            return None

        # list from closest to furthest taxi
        enough_seats_taxis.sort(
            key=lambda taxi: self.__env.get_distance(
                taxi.get_pos(), customer.get_start()
            )
        )

        # inform taxi to pick up customer
        for taxi in enough_seats_taxis:
            print(f"broker sending request for ride to {taxi}")
            result = taxi.receive_request("request for ride")
            print(f"{taxi} received request for ride from broker for {customer}")
            self.__message_sent += 1
            self.__message_received += 1
            if result:
                print(f"{taxi} accepted request for ride from broker for {customer}")
                new_ride = Ride(customer, taxi, self.__env)
                customer.ride_accepted()

                self.__message_sent += 1
                return new_ride
            else:
                print(f"{taxi} rejected request for ride from broker for {customer}")
                self.__message_received += 1

        customer.ride_rejected()
        self.__message_sent += 1
        return None
