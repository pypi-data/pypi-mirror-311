import time

booking_notification = [
    "Your seat is booked succesfully",
]

def booking_success():
    for notification in booking_notification:
        print(notification)
        return notification
    
booking_success()