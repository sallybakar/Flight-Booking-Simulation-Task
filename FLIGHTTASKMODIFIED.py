# Flight Booking Simulation
# Loading of libraries
import random
import string

# Defining Class Func

class FlightBookingSystem:
    def __init__(self):
        self.bookings = {}
        self.ticket_counter = 1
        self.user_emails = {}  # Dictionary to store mapping between emails and users

        
        # Generate a ticket number based on the destination
    def generate_ticket_number(self, destination, flight_class):
        ticket_number = f"{destination[:3]}-{flight_class}"
        return ticket_number
    
        # Generate a seat number based on the destination
    def generate_seat_number(self, destination):
        seat_number = f"{destination[:3]}-{self.ticket_counter:03d}"
        self.ticket_counter += 1
        return seat_number
    
        
    def book_flight(self, user, airline, destination, trip_type, account_balance, email):
        # Check if the email is already associated with a booking
        if any(booking['Email'] == email for booking in self.bookings.values()):
            print("This email is already associated with a booking. Please use a different email.")
            return

        if airline in airlines and destination in airlines[airline]:
            base_cost = airlines[airline][destination]["Cost"]
            timeline = airlines[airline][destination]["Timeline"]
            
            # Check if it's an urgent flight and adjust the cost accordingly
            is_urgent = input("Is this an urgent flight? (yes/no): ").lower()

            # Additional cost for urgent flights (you can adjust this value)
            urgent_multiplier = 2 if is_urgent == "yes" else 1

            # Add an additional cost for urgent flights based on trip type and flight class
            if trip_type.lower() == "one-way":
                trip_type_multiplier = 1
            elif trip_type.lower() == "two-way":
                trip_type_multiplier = 2
            else:
                print("Invalid trip type. Choose 'one-way' or 'two-way'.")
                return

            if flight_class.lower() == "economy":
                class_multiplier = 1
            elif flight_class.lower() == "business":
                class_multiplier = 2
            else:
                print("Invalid flight class. Choose 'economy' or 'business'.")
                return

            cost = base_cost * urgent_multiplier * trip_type_multiplier * class_multiplier

                # Assign a ticket and seat number
            if account_balance >= cost:
                ticket_number = self.generate_ticket_number(destination, flight_class)
                seat_number = self.generate_seat_number(destination)
                booking_details = {
                    "Airline": airline,
                    "Destination": destination,
                    "Trip Type": trip_type,
                    "Cost": cost,
                    "Timeline": timeline,
                    "Ticket Number": ticket_number,
                    "Seat Number": seat_number,
                    "Email": email,  # Add email to the booking details
                }
                self.bookings[user] = booking_details
                self.user_emails[email] = user  # Add the email-user mapping

                # Deduct the cost from the account balance
                account_balance -= cost

                # Print booking receipt
                print(f"Booking successful! ✈ Thank you for booking with us!  #{cost} deducted from your account.")
                print(f"Trip Details - Destination: {destination}, Type: {trip_type}, Timeline: {timeline}")
                print(f"Ticket Number: {ticket_number}, Seat Number: {seat_number}")
                print(f"Remaining Account Balance: #{account_balance:.2f}")
            else:
                print("Insufficient account balance.")
        else:
            print("Invalid airline or destination.")

             # func to cancel flight
    def cancel_flight(self, user, account_balance_input):
        if user in self.bookings:
            # Remove the email-user mapping
            email = [key for key, value in self.user_emails.items() if value == user]
            if email:
                del self.user_emails[email[0]]

            cancelled_booking = self.bookings.pop(user)
            cancellation_cost = cancelled_booking.get("Cost", 0)

            # Add the cancellation cost back to the account balance
            #account_balance_input += cancellation_cost

            # Print flght cancellation receipt
            print(f"Booking cancelled for {user}.")
            print("Cancelled Booking Details:", cancelled_booking)
            print(f"Cancellation Cost Returned: #{cancellation_cost:.2f}")
            print(f"Remaining Account Balance: #{account_balance_input:.2f}")

            # Return the updated account balance
            return account_balance_input
        else:
            print(f"No booking found for {user}.")

            # func to reschedule flight
    def reschedule_flight(self, user, new_timeline):
        if user in self.bookings:
            self.bookings[user]["Timeline"] = new_timeline
            print(f"Flight rescheduled for {user}. New timeline: {new_timeline}")
        else:
            print(f"No booking found for {user}.")

        # func to retrieve booking receipt
    def retrieve_booking_receipt(self, user):
        if user in self.bookings:
            print(f"Booking Receipt for {user}:")
            print(self.bookings[user])
        else:
            print(f"No booking found for {user}.")


# Example usage:
# Dictionary to store airlines and their codes along with seat capacity
airlines = {
    "Air-Peace": {"Lagos-Abuja": {"Cost": 55000, "Timeline": "09:00 AM - 03:00 PM"},
                  "Abuja-Lagos": {"Cost": 60000, "Timeline": "08:00 AM - 02:00 PM"},
                  "Port Harcourt-Abuja": {"Cost": 62000, "Timeline": "07:00 AM - 01:00 PM"},
                  "Kano-Lagos": {"Cost": 58000, "Timeline": "06:00 AM - 12:00 PM"},
                  "Imo-Lagos": {"Cost": 59000, "Timeline": "05:00 AM - 11:00 AM"},
                  "Anambra-Abuja": {"Cost": 57000, "Timeline": "07:00 AM - 01:00 PM"},
                  "Ekiti-Imo": {"Cost": 56000, "Timeline": "07:00 PM - 01:00 AM"}},

    "Arik-Air": {"Lagos-Abuja": {"Cost": 53000, "Timeline": "09:00 AM - 03:00 PM"},
                  "Abuja-Lagos": {"Cost": 57000, "Timeline": "08:00 AM - 02:00 PM"},
                  "Port Harcourt-Abuja": {"Cost": 59000, "Timeline": "07:00 AM - 01:00 PM"},
                  "Kano-Lagos": {"Cost": 55000, "Timeline": "06:00 AM - 12:00 PM"},
                  "Imo-Lagos": {"Cost": 56000, "Timeline": "05:00 AM - 11:00 AM"},
                  "Anambra-Abuja": {"Cost": 54000, "Timeline": "07:00 AM - 01:00 PM"},
                  "Ekiti-Imo": {"Cost": 53000, "Timeline": "07:00 PM - 01:00 AM"}},

            # Add more airlines, destinations, and details as needed
}


def display_destinations(airline):
    print(f"Available Destinations for {airline}:")
    destinations = airlines[airline]
    for i, destination in enumerate(destinations, 1):
        print(f"{i}. {destination}")

def get_destination_choice(airline):
    while True:
        try:
            choice = int(input(f"Enter the number of your desired destination for {airline}: "))
            destinations = airlines[airline]
            if 1 <= choice <= len(destinations):
                return list(destinations.keys())[choice - 1]
            else:
                print("Invalid choice. Please enter a number within the provided range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


booking_system = FlightBookingSystem()
# Loop to simulate flight bookings
while True:
    print("\n🛫 Welcome to the Flight Booking System!")
    print("\n✈nFlight Booking Menu:")
    print("1. Book a Flight")
    print("2. Cancel a Flight")
    print("3. Reschedule Flight")
    print("4. Retrieve Booking Receipt")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    # Book a flight
    if choice == "1":
        print("\n🛫 Welcome to the Flight Booking System!")
        user = input("Enter your name: ")
        num = input("Enter your phone number: +234-")

        # Validate email format
        while True:
            email = input("Enter your email address: ")
            if '@' in email and '.' in email:
                break
            print("Invalid email format. Please provide a valid email address.")

        # Check if the airline exists (dummy check)
        print("Available Airlines:")
        for airline, destinations in airlines.items():
            print(airline)
        # Ask the user to enter a valid airline
        airline = input("Enter your preferred airline: ")

        # Display and get the destination choice
        display_destinations(airline)
        destination = get_destination_choice(airline)
       
        # Ask the user to enter trip type, account balance input, and flight class
        trip_type = input("Enter trip type (one-way/two-way): ")
        account_balance_input = float(input("Enter your account balance: #"))
        flight_class = input("Enter the class of the flight (economy/business): ")

        # Call the book_flight func
        booking_system.book_flight(user, airline, destination, trip_type, account_balance_input, email)

        # Cancel a flight reservation
    elif choice == "2":
        user = input("Enter your name: ")

        # Call the cancel_flight func
        booking_system.cancel_flight(user, account_balance_input)

        # Reschedule Flight
    elif choice == "3":
        user = input("Enter your name: ")
        new_timeline = input("Enter the new timeline for your flight: ")

        # Call the reschedule_flight func
        booking_system.reschedule_flight(user, new_timeline)

        # To Retrieve Booking Receipt when lost or misplaced
    elif choice == "4":
        identifier = input("Enter your name: ")

        # Call the retrieve_booking_receipt func
        booking_system.retrieve_booking_receipt(identifier)

    # To Exit the Flight Booking System
    elif choice == "5":
        print("Exiting Flight Booking System. Thank you!")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")