from django.conf import settings
from twilio.rest import Client
import random
from loginapp.models import User


class MessageHandler:
    phone_number = None
    otp = None
    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number
        self.otp = random.randint(1000,9999)

    def send_otp_to_phone(self):
        client = Client(settings.account_sid,settings.auth_token)

        message = client.messages \
                        .create(
                            body=f"your otp is {self.otp}",
                            from_='+17078778695',
                            to=self.phone_number
                        )
        user_obj = User.objects.get(email=data['to_email'])
        

        print(message.sid)


from Appointment. models import *
from Appointment.serializer import *
def setUseravalibilty(user_id):
    print(user_id)
    data = {}
    data["user_id"] = user_id
    from datetime import date
    from dateutil.relativedelta import relativedelta
    today = date.today()
    data["start_Date"] = today
    after_one_month = today + relativedelta(months=1)
    data["end_Date"] = after_one_month
    start_time = "09:00:00"
    data["start_Time"] = start_time
    end_time = "21:00:00"
    data["end_Time"] = end_time

    user_data = UserAvailabilty.objects.filter(user_id = user_id)
    if user_data:
        user_data = UserAvailabilty.objects.filter(user_id = user_id).update(start_Date = today, end_Date = after_one_month, start_Time = start_time, end_Time = end_time , user_id = user_id)
        print(user_data)
    else:
        print(data)
        serializer = UserAppointmentSerilizer(data=data)
        if serializer.is_valid():
            serializer.save()
    print('new date is')