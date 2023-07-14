from django.http import Http404
from rest_framework import status
from itertools import chain
from rest_framework.parsers import FormParser, MultiPartParser
from questionair.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Notifications.push_notification import Push_notifications
# from loginapp.models import *
from django.contrib.auth.models import User
from loginapp.models import User
# from listing.models import *
from rest_framework.views import APIView
from Notifications.serializer import NotificationsSerializer
from rest_framework import generics





class getQuestionView(APIView):
    serializer_class = QuestionSerializer
    parser_classes = (FormParser, MultiPartParser)


    def get_object(self):
        try:
            return question.objects.get(id=self.kwargs.get('pk'))
        except question.DoesNotExist:
            raise Http404

    def get(self, request):
        try:
            question_list = {}
        # snippet = self.get_object()
            question_type = "Rental_Listings"
            Rental_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Rental_Listings'] = Rental_Listings
            question_type = "Sales_Listings"
            Sales_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Sales_Listings'] = Sales_Listings
            print(Sales_Listings)
            # serializer = self.serializer_class(snippet)
            return Response(question_list)
        except question.DoesNotExist:
            raise Http404
        


class ListingAnswer(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListingQuestionSerializer
    # parser_classes = (FormParser, MultiPartParser)


    def post(self, request):
        try:
            user = request.user.id
            question_list = {}
            data = request.data
            print(data)
            question = data['question']
            print(question)
            listing_id = data['listing']
            query=listing.objects.filter(id = listing_id).values().first()
            if query["user_id_id"] == user:
                exist_query= ListingQuestion.objects.filter(listing_id =listing_id ).values().first()
                if not exist_query:
                    for i in question:
                        question_list['question'] = i['id']
                        question_list['listing'] = listing_id
                        question_list['expected_Answer'] = i['ans']
                        serializer = self.serializer_class(data=question_list)
                        # print(serializer.data)
                        if  serializer.is_valid(raise_exception=True):
                            serializer.save() 
                            pass
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.data)
                else:
                    delete_data=ListingQuestion.objects.filter(listing_id = listing_id).delete()
                    for i in question:
                        question_list['question'] = i['id']
                        question_list['listing'] = listing_id
                        question_list['expected_Answer'] = i['ans']
                        serializer = self.serializer_class(data=question_list)
                        # print(serializer.data)
                        if  serializer.is_valid(raise_exception=True):
                            serializer.save() 
                            pass
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.data)

            else:
                return Response(status=status.HTTP_409_CONFLICT)
        except ListingQuestion.DoesNotExist:
            raise Http404



class InterestedAnswer(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = interestedAnswerSerializer
    interested_user = interestedUserSerializer
    # parser_classes = (FormParser, MultiPartParser)
    
    def post(self, request):
        user_inter = {}
        try:
            interested_list = {}
            data = request.data
            print(data)
            question = data['question']
            listing = data['listing']
            user_ans =ListingQuestion.objects.filter(listing = listing).values()
            owner_id = data['owner_id']
            user_id = data['user_id']
            future_ans = data['future_ans']
            match = True
            for i in question:
                interested_list['question'] = i['id']
                interested_list['choice_text'] = i['ans']
                interested_list['listing'] = listing
                interested_list['owner_id'] = owner_id
                interested_list['user_id'] = user_id
                interested_list['save_in_future'] = future_ans
                serializer = self.serializer_class(data=interested_list)
                if  serializer.is_valid(raise_exception=True):
                    serializer.save() 
                    for j in user_ans:
                        que_id = str(j['question_id'])
                        if  i['id'] == que_id:
                            inter_ans = i['ans']
                            inter_ans = inter_ans.lower()
                            expec_ans = j["expected_Answer"]
                            expec_ans = expec_ans.lower()
                            if inter_ans != expec_ans :
                                match = False

            
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            user_inter["listing_id"] = listing
            user_inter["interested_user_id"] = user_id
            user_inter["match_ans"] = match
            user_inter["listing_owner_id"] = owner_id

            serializer1 = self.interested_user(data = user_inter)
            if serializer1.is_valid(raise_exception=True):
                serializer1.save()
                pass
            title= "New Property Interest"
            body = "A new interest is submitted on your listing"
            data ={
                "listing_id": listing,
                "interested_user_id": user_id,
                "listing_owner_id":owner_id,
            }
            type = "interest"
            Push_notifications(title, body, owner_id, type, data)
            return Response(status=status.HTTP_201_CREATED)
        except interestedAnswer.DoesNotExist:
            raise Http404






class RequestquestionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, user):
        try:
            return User.objects.filter(id=user).values()
        except question.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user.id
        print(user)
        try:
            question_list = {}
            id = listing.objects.filter(user_id_id = user).values('id')
            for i in id:
                user_ans = ListingQuestion.objects.filter(listing = i['id'] ).values()
                # print(user_ans , "user")
                inter_ans = interestedAnswer.objects.filter(listing_id = i['id']).values()
                # print(inter_ans , "interested")
                # for user in user_ans:
                #     que = user['question_id']
                #     for ans in inter_ans:
                #         print(ans['question_id'], "ans")
                #         if ans['question_id'] == que:
                #             if ans["choice_text"] == user['expected_Answer']:
                #                 print("i love you")
                #         else:
                #             print("i hate you")

                        # for j in ans:
                        #     print(j['question_id'],"121")
                        #     if j['question_id'] == que:
                        #         print("121")
                                # if j["choice_text"] == user["expected_Answer"]:
                                #     print("12")
            return Response(question_list)
        except question.DoesNotExist:
            raise Http404
        

class getinterestedrequest(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = interestedUserSerializer
    def get(self, request, *args, **kwargs):
        result_list = []
        user = self.request.user.id
        is_match = self.request.query_params.get('is_match')
        queryset  =interestedUser.objects.filter(listing_owner_id=user, match_ans = is_match).values()
        print(queryset, "quest")
        for i in queryset:
            print(i)
            request_value = {}
            interested_user_id =i['interested_user_id_id']
            listing_owner_id =i['listing_owner_id_id']
            listing_id = i['listing_id_id']
            interested_user=User.objects.filter(id = interested_user_id).values("username",'profile_image','phone_number').first()
            list = listing.objects.filter(id = listing_id ).values().first()
            request_value["user"] = interested_user
            request_value['data1'] = i
            request_value["list"] = list
            print(request_value)
            result_list.append(request_value)
        return Response(result_list)



class isrequest(APIView):
    # permission_classes = [IsAuthenticated]    
    def put(self,request):
        data = request.data
        id = data['id']
        is_request = data['is_request']
        update_query = interestedUser.objects.filter(id = id).update(is_request = is_request)
        query = interestedUser.objects.filter(id = id).values().first()
        print(query)
        title= "Property Interest Request Approve"
        body = "Your request on listing is approved"
        notification_data = query
        type = "interested_request"
        Push_notifications(title, body,query["interested_user_id_id"], type, notification_data)
        return Response(query)

class getAllAttachedAnswer(APIView):
    serializer_class = interestedUserSerializer
    interested_serializer_class = interestedAnswerSerializer

    def get(self, request):
        user_id = self.request.query_params.get('user_id')
        listing = self.request.query_params.get('listing')
        query=interestedAnswer.objects.all().values("choice_text")
        print(query)
        data=interestedAnswer.objects.filter(user_id_id = user_id , listing = listing).values()
        if data:
            return Response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class getmyinterestedquestion(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = interestedUserSerializer
    def get(self, request, *args, **kwargs):
        result_list = []
        user = self.request.user.id
        queryset  =interestedUser.objects.filter(interested_user_id=user).values()
        for i in queryset:
            request_value = {}
            user3 =i['interested_user_id_id']
            listing_id = i['listing_id_id']
            user1=User.objects.filter(id = user3).values("username",'profile_image','phone_number').first()
            list = listing.objects.filter(id = listing_id ).values().first()
            request_value["user"] = user1
            request_value['data1'] = i
            request_value["list"] = list
            print(request_value)
            result_list.append(request_value)
        return Response(result_list)





