from django.http import Http404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from questionair.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from loginapp.models import *
from rest_framework.views import APIView




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
            question_type = "Rental Listings"
            Rental_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Rental Listings'] = Rental_Listings
            question_type = "Sales Listings"
            Sales_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Sales Listings'] = Sales_Listings
            print(Sales_Listings)
            # serializer = self.serializer_class(snippet)
            return Response(question_list)
        except question.DoesNotExist:
            raise Http404
        


class ListingAnswer(APIView):
    serializer_class = ListingQuestionSerializer
    # parser_classes = (FormParser, MultiPartParser)


    def post(self, request):
        try:
            question_list = {}
            data = request.data
            question = data['question']
            listing = data['listing']
            for i in question:
                question_list['question'] = i['id']
                question_list['listing'] = listing
                question_list['expected_Answer'] = i['ans']
                serializer = self.serializer_class(data=question_list)
                # print(serializer.data)
                if  serializer.is_valid(raise_exception=True):
                    serializer.save() 
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        except ListingQuestion.DoesNotExist:
            raise Http404



class InterestedAnswer(APIView):
    serializer_class = interestedAnswerSerializer
    interested_user = interestedUserSerializer
    # parser_classes = (FormParser, MultiPartParser)
    
    def post(self, request):
        user_inter = {}
        try:
            interested_list = {}
            data = request.data
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
            serializer1 = self.interested_user(data = user_inter)
            if serializer1.is_valid(raise_exception=True):
                serializer1.save()
                pass
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
                print(user_ans , "user")
                inter_ans = interestedAnswer.objects.filter(listing_id = i['id']).values()
                print(inter_ans , "interested")
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
        