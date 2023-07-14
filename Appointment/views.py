from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework import status
from .generateSlots import get_daily_slots
from Notifications.push_notification import Push_notifications
from rest_framework.views import APIView
from .models import *
from .serializer import *

# Create your views here.
# class AppointmentView(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerilizer
#     permission_classes = [IsAuthenticated]


class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerilizer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            title= "New Appointment Request"
            body = "New appointment request is submitted on your listing"
            type = "Appointment"
            data = request.data
            listing_owner_id = data["Listing_Owner_Id"]
            Push_notifications(title, body, listing_owner_id, type, data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetMySentAppointment(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerilizer

    def get(self, request):
        id =self.request.user.id
        mySentAppointment = {}
        query=Appointment.objects.filter(user_id = id).values()
        appointment = []
        for i in query:
            print(i["listing_id_id"])
            getRecviedAppointment = {}
            data = listing.objects.filter(id = i["listing_id_id"]).values().first()
            getRecviedAppointment["listing"] = data
            listing_images=Listing_Media.objects.filter(listing = i["listing_id_id"]).values('images_Url')
            getRecviedAppointment["listing_images"] = listing_images
            getRecviedAppointment["appointmentData"] = i
            appointment.append(getRecviedAppointment)
        return Response(appointment)

class getUserAvailabilty(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerilizer
    def get(self, request):
        user_id = self.request.user.id
        user_data = UserAvailabilty.objects.filter(user_id = user_id).values()
        if user_data:
            return Response(user_data)
        return Response(status=status.HTTP_200_OK)
        
        





class GetRecviedAppointmentRequest(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerilizer

    def get(self, request):
        id =self.request.user.id
        query=Appointment.objects.filter(Listing_Owner_Id = id).values()
        # getRecviedAppointment["MySentAppointment"] = query
        appointment = []
        for i in query:
            print(i["listing_id_id"])
            getRecviedAppointment = {}
            data = listing.objects.filter(id = i["listing_id_id"]).values().first()
            listing_images=Listing_Media.objects.filter(listing = i["listing_id_id"]).values('images_Url')
            getRecviedAppointment["listing_images"] = listing_images
            getRecviedAppointment["listing"] = data
            getRecviedAppointment["appointmentData"] = i
            appointment.append(getRecviedAppointment)
        return Response(appointment)




class UserAvailabiltyView(APIView):
    serializer_class = UserAppointmentSerilizer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user_id = data['user_id']
        user_data = UserAvailabilty.objects.filter(user_id = user_id)
        if user_data:
            user_data = UserAvailabilty.objects.filter(user_id = user_id).update(start_Date = data["start_Date"], end_Date = data["end_Date"], start_Time = data["start_Time"], end_Time = data["end_Time"] , user_id = user_id)
            result = UserAvailabilty.objects.filter(user_id = user_id).values()
            return Response(result)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerilizer
    def put(self,request):
        user_id = request.user.id
        data = request.data
        print(data)
        appointment_id = data['id']
        is_Confirmed = data["is_Confirmed"]
        status = data["status"]
        query = Appointment.objects.filter(id = appointment_id, Listing_Owner_Id_id = user_id).update(is_Confirmed = is_Confirmed, status = status)
        appointment_data = Appointment.objects.filter(id = appointment_id).values().first()
        print(appointment_data)

        if is_Confirmed == "True" and appointment_data:
            title= "Appointment Approved"
            body = "Your appointment request is approved"
            type = "Appointment"
            notification_data = appointment_data
            notification_user = appointment_data["user_id_id"]
            Push_notifications(title, body, notification_user, type, notification_data)
        return Response(data)
        

class UpdateUserAvailabiltyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAppointmentSerilizer
    def put(self,request):
        id = request.user.id
        data = request.data
        is_Confirmed = data["is_Confirmed"]
        status = data["status"]
        query = Appointment.objects.filter(Listing_Owner_Id = id).update(is_Confirmed = is_Confirmed, status = status)
        data = Appointment.objects.filter(Listing_Owner_Id = id)
        return Response(data)


class getAvailableTimeSlot(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = UserAppointmentSerilizer
    def get(self, request):
        try:
            date = self.request.query_params.get('selected_date')
            selected_date = datetime.strptime(date,  '%Y-%m-%d').date()
            listing_Owner_Id  = self.request.query_params.get('listing_Owner_Id')
            query = UserAvailabilty.objects.filter(user_id = listing_Owner_Id).values().first()
            # listing_Owner_Id  = self.request.query_params.get('listing_id')
            start_time =query['start_Time']
            end_Time =query['end_Time']
            current_time = datetime.now().time().strftime("%H:%M:%S")
            time_object = datetime.strptime(current_time, '%H:%M:%S').time()
            timeSLot = 60
            if start_time <= time_object and time_object <= end_Time:
                start_time= start_time.strftime("%H:%M")
                time_object= time_object.strftime("%H:%M")
                end_Time= end_Time.strftime("%H:%M")
                all_time_slot= get_daily_slots(start=time_object, end=end_Time, slot=timeSLot, date=selected_date)
                book_time_slot=Appointment.objects.filter(appointment_Date = date , Listing_Owner_Id =listing_Owner_Id).values()
                print(all_time_slot, "alltime")
                AvailableSlots = []
                for i in all_time_slot:
                    time =  i.time()
                    
                    if book_time_slot :
                        for book in book_time_slot:
                            print("slot not avaliable", book["appointment_Time"])
                            if book["appointment_Time"] == time:
                                print("slot not avaliable", book["appointment_Time"] , time)
                            else: 
                                AvailableSlots.append(i)
                    else:
                        AvailableSlots.append(i)
                print(current_time)
                Final_AvailableSlots= set(AvailableSlots)
                return Response(Final_AvailableSlots)
            return Response(status=status.HTTP_200_OK)
            
        except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_200_OK)


        # start_time = '9:00'
        # end_time = '15:00'
        # timeSLot = 30
        # days = 2
        # start_date = datetime.now().date()

        # for i in range(days):
        #     date_required = datetime.now().date() + timedelta(days=1)
        #     print(get_daily_slots(start=start_time, end=end_time, slot=timeSLot, date=date_required))

