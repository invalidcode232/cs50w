class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, passenger):
        if not self.open_seats():
            return False

        self.passengers.append(passenger)
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)
flight.add_passenger("Harry")
flight.add_passenger("Harry")

print(flight.passengers)
print(flight.open_seats())