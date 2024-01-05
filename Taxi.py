from Ride import Ride
class Taxi:
    def __init__(self, id, pos, seats, env):
        self.__id = id
        self.__pos = pos
        self.__seats = seats
        self.__idle = True
        self.__env = env

    def receive_request(self, message: str):
        """
        parameters:
            message: string
        returns:
            True if the taxi is idle and accepted the request
            False otherwise
        """
        if self.__idle:
            self.__idle = False
            return True
        return False

    def create_ride(self,customer):
        new_ride = Ride(customer,self,self.__env)
        return new_ride
    
    def get_pos(self):
        return self.__pos

    def get_seats(self):
        return self.__seats

    def set_pos(self, pos):
        self.__pos = pos

    def get_id(self):
        return self.__id

    def set_idle(self):
        self.__idle = True

    def __repr__(self):
        return f"Taxi {self.__id} at {self.__pos} with {self.__seats} seats"
