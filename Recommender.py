from Taxi import Taxi
from Customer import Customer


class Recommender:
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
        """
        print(f"Recommender received message {message} from {customer}")
        self.__message_received += 1
        if message == "request":
            return self.recommend_taxis(customer)
    
    def recommend_taxis(self,customer: Customer):
        """
        The recommender sends the list of available taxis to the customer
        parameters:
            customer: Customer object
            message: string
        returns:
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
        return enough_seats_taxis