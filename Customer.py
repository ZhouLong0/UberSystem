class Customer:
    def __init__(self, id, start, dest, req_seats):
        self.__id = id
        self.__start = start
        self.__dest = dest
        self.__req_seats = req_seats
        self.__idle = True
        self.__finished = False

    def send_message(self, broker, message: str):
        print(f"{self} sent message {message} to broker")
        return broker.receive_message(self, message)

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
