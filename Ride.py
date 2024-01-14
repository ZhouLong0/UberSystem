from Environment import Environment


class Ride:
    """
    Represents a ride from a customer's start to destination
    """

    def __init__(self, customer, taxi, env: Environment):
        self.__customer = customer
        self.__taxi = taxi
        self.__start = taxi.get_pos()
        self.__pickup_pos = customer.get_start()
        self.__destination = customer.get_dest()

        self.__current_pos = self.__start

        self.__env = env
        self.__is_finished = False
        self.duration = 0

        # path from start to pickup_pos to destination
        self.path = env.astar(self.__start, self.__pickup_pos)[::-1]
        path2 = env.astar(self.__pickup_pos, self.__destination)[::-1]
        self.path += path2

    def move(self):
        """
        Move the taxi, customer in the ride to the next position
        """
        if self.__current_pos == self.__pickup_pos:
            print(
                f"customer {self.__customer.get_id()} picked up by taxi {self.__taxi.get_id()}"
            )

        if self.__current_pos == self.__destination:
            print(
                f"customer {self.__customer.get_id()} dropped off by taxi {self.__taxi.get_id()}"
            )
            self.__is_finished = True
            self.__customer.set_finished()
            self.__taxi.set_idle()
            return

        self.__current_pos = self.path.pop(0)
        self.__taxi.set_pos(self.__current_pos)
        self.duration += 1

    def is_finished(self):
        return self.__is_finished

    def get_customer(self):
        return self.__customer

    def __repr__(self) -> str:
        return f"Ride from {self.__start} to {self.__pickup_pos} to {self.__destination}, current position: {self.__current_pos}, path: {self.path}, customer: {self.__customer}, taxi: {self.__taxi}"
