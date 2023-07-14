from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
import json
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from .serializers import *
from django.db.models import Q
from listing.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from .mypagination import myCursorPagination
from django.db.models import Max
from .models import *
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class FavouriteView(APIView):
    serializer_class = FavouriteListingSerializer
    list_serializer_class = getListingSerializer

    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)


    def get(self, request):
        user = request.user.id
        print(user)
        favorate_list = []
        listing_data = []
        snippet=FavouriteListing.objects.filter(user = user , status = True).values()
        print(snippet, "helo")
        if snippet:
            for i in snippet:
                print(i)
                listing_data = listing.objects.filter(id = i["listing_id"])
                if listing_data:
                        for j in listing_data:
                            # print(i)
                            serializer = self.list_serializer_class(j)
                            pub=Listing_Amenities.objects.filter(listing =  j.id).select_related("Amenities_ID").values("Amenities_ID__id","Amenities_ID__Amenities_Name" )
                            data = serializer.data
                            print(data)
                            data['Amenities_ID__Amenities_Name'] = pub
                            favorate_list.append(data)
                            print(favorate_list)
            return Response(favorate_list, status=status.HTTP_200_OK) 
               
        else:
            return Response({"message":"no listing"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user.id
        request.data._mutable=True
        data = request.data
        data["user"] = user
        request.data._mutable = False
        data = request.data
        query=FavouriteListing.objects.filter(user = user, listing = data["listing"])
        serializer = self.serializer_class(data=data)
        if query:
            status=FavouriteListing.objects.filter(user = user, listing = data["listing"]).update(status = data['status'])
            query=FavouriteListing.objects.filter(user = user, listing = data["listing"]).values()
            return Response(query)
        else:
            if serializer.is_valid(raise_exception=True):
                serializer.save() 
            return Response(serializer.data)


class checkfavouaite(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user.id
        print(user)
        snippet=FavouriteListing.objects.filter(user = user).values('status')
        if snippet:
            return Response(snippet, status = status.HTTP_200_OK)
        return Response(status = status.HTTP_404_NOT_FOUND)

