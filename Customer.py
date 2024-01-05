
class Customer:
    def __init__(self, id, start, dest, req_seats):

        self.__id = id
        self.__start = start
        self.__dest = dest
        self.__req_seats = req_seats
        self.__idle = True
        self.__finished = False
        self.__message_received = 0
        self.__message_sent = 0

    def send_message(self, broker, message: str):
        print(f"{self} sent message {message} to broker")
        return broker.receive_message(self, message)
    
    def ask_recommendation(self, recommender, message: str):
        print(f"{self} sent message {message} to recommender")
        enough_seats_taxis = recommender.receive_message(self, message)
        if enough_seats_taxis is not None:
            return self.receive_recommendation(enough_seats_taxis)
        else:
            return None


    
    
    def receive_recommendation(self,enough_seats_taxis):
        """
        parameters:
            enough_seat_taxis: list of taxis with enough seats

        tries to request a ride to all of the taxis, don't know if they accept or not (free or not)
        returns:
            Ride object if a taxi accepted the request
            None otherwise
        """
        for taxi in enough_seats_taxis:
            print(f"customer sending request for ride to {taxi}")
            result = taxi.receive_request("request for ride")
            print(f"{taxi} received request for ride from broker for {self}")
            self.__message_sent += 1
            self.__message_received += 1
            if result:
                print(f"{taxi} accepted request for ride from broker for {self}")
                new_ride = taxi.create_ride(self)
                self.ride_accepted()
                self.__message_sent += 1
                return new_ride
            else:
                print(f"{taxi} rejected request for ride from broker for {self}")
                self.__message_received += 1

        self.ride_rejected()
        self.__message_sent += 1
        return None        


    def ride_accepted(self):
        self.__idle = False
        print(f"{self} ride accepted")

    def ride_rejected(self):
        self.__request_sent = False
        print(f"customer {self} ride rejected, waiting to request again")

    def get_dest(self):
        return self.__dest

    def get_start(self):
        return self.__start

    def is_idle(self):
        return self.__idle

    def get_req_seats(self):
        return self.__req_seats

    def get_id(self):
        return self.__id

    def set_finished(self):
        self.__finished = True

    def __repr__(self):
        return f"Customer {self.__id} from {self.__start} to {self.__dest} with {self.__req_seats} seats"

    def is_finished(self):
        return self.__finished
