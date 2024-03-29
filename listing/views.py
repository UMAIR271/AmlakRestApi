
from django.http import Http404
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from favourite.models import *
from listing.serializers import *
from django.db.models import Q
from questionair.models import *
from listing.models import listing
from rest_framework import viewsets
from rest_framework.response import Response
from .mypagination import MyCursorPagination
from loginapp.models import *
from django.http import QueryDict
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .helper import *

class ListingView(viewsets.ModelViewSet):
    queryset = listing.objects.all()
    serializer_class = getListingSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = MyCursorPagination

    
class getallListing(APIView, MyCursorPagination):
    def get(self, request):
        user_id = self.request.query_params.get('user_id')
        data=listing.objects.all()
        paginated_queryset=self.paginate_queryset(data, request, view=self)
        serializer = getListingSerializer(paginated_queryset, many=True)
        if user_id:
            for i in serializer.data:
                listing_id = i['id']
                favouriteListing = FavouriteListing.objects.filter(listing = listing_id , user = user_id).values().first()
                i["favouriteListing"] = favouriteListing
        return self.get_paginated_response(serializer.data)
        
        



class GetListingView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = getListingSerializer
    def get_object(self):
        try:
            return listing.objects.get(id=self.kwargs.get('pk'))
            
        except listing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        attach = []
        print(pk)
        user_id = self.request.query_params.get('user_id')
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        pub=Listing_Amenities.objects.filter(listing =  pk).select_related("Amenities_ID").values("Amenities_ID__id","Amenities_ID__Amenities_Name" )
        data = serializer.data
        data['Amenities_ID__Amenities_Name'] = pub
        attached_ques = ListingQuestion.objects.filter(listing_id = pk).values()
        data["attached_question"] = attached_ques
        if user_id:
          interested_data = interestedUser.objects.filter(interested_user_id = user_id, listing_id = pk ).values().first()
          data["interested_data"] = interested_data
          favouriteListing = FavouriteListing.objects.filter(listing = pk , user = user_id).values().first()
          data["favouriteListing"] = favouriteListing
        return Response(data)

    def put(self, request, pk):
        object = self.get_object()
        v1 = []
            # id = Listing_Amenities.objects.filter(listing=self.kwargs.get('pk'))
        var = Listing_Amenities.objects.select_related().filter(listing = pk)
        print(var)
        for i in var:
            print(i.Amenities_ID)
        data=Amenities.objects.filter(id = 2).values("Amenities_Name")
        v1.append(data)
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MylistingView(APIView):
    serializer_class = getListingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        try:
            mylisting = []
            user = request.user.id
            listing_data = listing.objects.filter(user_id = user)
            if listing_data:
                for i in listing_data:
                    serializer = self.serializer_class(i)
                    pub=Listing_Amenities.objects.filter(listing =  i.id).select_related("Amenities_ID").values("Amenities_ID__id","Amenities_ID__Amenities_Name" )
                    data = serializer.data
                    data['Amenities_ID__Amenities_Name'] = pub
                    favouriteListing = FavouriteListing.objects.filter(listing = i.id, user = user).values().first()
                    data["favouriteListing"] = favouriteListing
                    mylisting.append(data)

                return Response(mylisting) 
            else:
                return Response({"message":"no listing"}, status=status.HTTP_404_NOT_FOUND) 
        except listing.DoesNotExist:
            raise Http404  
     
class ListMedia(generics.ListCreateAPIView):
    queryset = Listing_Media.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = Listing_MediaSerializer

class ListMediaUdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing_Media.objects.all()
    serializer_class = Listing_MediaSerializer

class FindProperty(APIView):
    serializer_class = getListingSerializer

    def get(self, request):
        search = self.request.query_params.get('query')
        user_id = self.request.query_params.get('user_id')
        try:
                query = listing.objects.filter(Q(project_name__contains = search) | Q(street_Address__contains = search))
                serializer = self.serializer_class(query,many=True)
                data = serializer.data
                if user_id:
                    for i in serializer.data:
                        listing_id = i['id']
                        favouriteListing = FavouriteListing.objects.filter(listing = listing_id , user = user_id).values().first()
                        i["favouriteListing"] = favouriteListing
                return Response(data)

        except listing.DoesNotExist:
            raise Http404

class AmenitiesView(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    parser_classes = (FormParser, MultiPartParser)


class ListingAmenitiesView(viewsets.ModelViewSet):
    queryset = Listing_Amenities.objects.all()
    serializer_class = ListingAmenitiesSerializer
    parser_classes = (FormParser, MultiPartParser)

class UpdateAmenitiesView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = AmenitiesSerializer

    def get_object(self):
        try:
            return Amenities.objects.get(id=self.kwargs.get('pk'))
        except Amenities.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        object = self.get_object()
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddListingPostData(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_list = postListingSerializer
    serializer_property = porpertyTypeSerializer
    serializer_image = Listing_MediaSerializer
    compress_serializer = CompressImageSerializer
    floorplane_serializer = floorplaneSerializer
    serializer_Amenities = ListingAmenitiesSerializer
    verifed_serializer = verifedImageSerializer
    parser_classes = (FormParser, MultiPartParser)

    
    def post(self, request):
        try:
            arr = []
            Amenities = ""
            images = ""
            floorPlaneImages = ""
            property = ""
            verify_images = ""
            data= request.data
            if 'images_Url' in str(data):
                images = dict((request.data).lists())['images_Url']
                data.pop("images_Url")
            else:
                 return Response({"message":"enter the image"}, status=status.HTTP_400_BAD_REQUEST)
            if 'floorPlaneImage' in str(data):
                floorPlaneImages = dict((request.data).lists())['floorPlaneImage']
                data.pop("floorPlaneImage")
            else:
                pass

            if 'Amenities_ID' in str(data):
                Amenities = dict((request.data).lists())['Amenities_ID']
                data.pop("Amenities_ID")
                            
            else:
                pass
            if 'property_type' in str(data):
                property = request.data['property_type']
                data.pop("property_type")

            else:
                pass
            if 'propertyVerificationImage' in str(data):
                verify_images = dict((request.data).lists())['propertyVerificationImage']
                data.pop("propertyVerificationImage")
            else:
                pass
            
            
            if data:
                serializer1 = self.serializer_list(data=data)
                if  serializer1.is_valid(raise_exception=True):
                    serializer1.save()  
                    id=serializer1.data['id']
                    cover_image ="https://umair2701.pythonanywhere.com/uploads/"+str(images[0])
                    slider = listing.objects.filter(id = id).update(cover_image = cover_image )
                    print(slider)
                else:
                        return Response({"message":"enter the listing"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                        return Response({"message":"enter the listing"}, status=status.HTTP_400_BAD_REQUEST)
                
            if images:
                for img_name in images:
                    modified_data = modify_input_for_multiple_files(id,img_name)
                    file_serializer =self.serializer_image(data=modified_data)
                    if file_serializer.is_valid(raise_exception=True):
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        print("umair")
                        return Response({"message":"enter the image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if Amenities:            
                for Amenities_name in Amenities:
                    Amenities_ID = Amenities_name
                    Amenities_ID=Amenities_ID.replace(',', '')
                    for Amenities_id in Amenities_ID:
                        modified_data = multiple_Amenaties(id,int(Amenities_id))
                        file_serializer =self.serializer_Amenities(data=modified_data)
                        if file_serializer.is_valid(raise_exception=True):
                            file_serializer.save()
                            arr.append(file_serializer.data)
                        else:
                            return Response({"message":"enter the Amenities"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                # return Response({"message":"enter the Amenities"}, status=status.HTTP_400_BAD_REQUEST)

            if property:
                modified_data = multiple_property(id,property)
                file_serializer =self.serializer_property(data=modified_data)
                if file_serializer.is_valid():
                    file_serializer.save()
                    arr.append(file_serializer.data)
                else:
                    return Response({"property":"enter the Property Name"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                    # return Response({"property":"enter the Property Name"}, status=status.HTTP_400_BAD_REQUEST)
            
            if floorPlaneImages:
                for floorImage in floorPlaneImages:
                    modified_data = floorPlans_multiple_files(id,floorImage)
                    print(modified_data)
                    file_serializer =self.floorplane_serializer(data=modified_data)
                    if file_serializer.is_valid():
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        return Response({"message":"enter the floor Plane Image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                # return Response({"message":"enter floor the image"}, status=status.HTTP_400_BAD_REQUEST)

            if verify_images:
                for verify_image in verify_images:
                    modified_data = verify_multiple_files(id,verify_image)
                    file_serializer =self.verifed_serializer(data=modified_data)
                    if file_serializer.is_valid():
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        return Response({"message":"enter the verify Plane Image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            return Response({"listing_id":id},status=status.HTTP_200_OK)
        except listing.DoesNotExist:
            raise Http404


class filterViewSet(generics.ListAPIView):
    queryset = listing.objects.all()
    serializer_class = filterserializers
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Purpose_Type','Type','property_pricing','property', 'size','Bedrooms','Batrooms','Project_status','Amenities__Amenities_Name']
 

class interestedLisitingView(viewsets.ModelViewSet):
    serializer_class = interestedListingSerializer
    queryset = interested.objects.all()
    parser_classes = (FormParser, MultiPartParser)



class getInterestedLisitingView(generics.UpdateAPIView):
    queryset = interested.objects.all()
    serializer_class = interestedListingSerializer
    parser_classes = (FormParser, MultiPartParser)


    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)



class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class UpdateAppointmentView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)


class SlotsView(viewsets.ModelViewSet):
    serializer_class = SlotstSerializer
    queryset = AvailableSlots.objects.all()

class filterView(generics.ListAPIView):
    model = listing
    serializer_class = getListingSerializer
    parser_classes = (FormParser, MultiPartParser)


    # Show all of the PASSENGERS in particular WORKSPACE
    # or all of the PASSENGERS in particular AIRLINE
    def get_queryset(self):
        try:
            queryset = listing.objects.all()
            check_Purpose_Type = self.request.query_params.get('check_Purpose_Type', None)
            check_Type = self.request.query_params.get('check_Type', None)
            check_property_Type = self.request.query_params.get('check_property_Type', None)
            min_price = self.request.query_params.get('min_price', None)
            max_price = self.request.query_params.get('max_price', None)
            check_property_size = self.request.query_params.get('check_property_size', None)
            check_bedroom = self.request.query_params.get('check_bedroom', None)
            check_batroom = self.request.query_params.get('check_batroom')
            check_project_status = self.request.query_params.get('check_project_status', None)
            check_Amenities = self.request.query_params.get('check_Amenities', None)
            if check_Amenities:
                check_Amenities=check_Amenities.replace(',', '')
                res = []
                for i in check_Amenities:
                    res.append(int(i))
                # data =  Listing_Amenities.objects.filter(listing__Purpose_Type = check_Purpose_Type, listing__Type = check_Type,listing__property__property_type = check_property_Type ).values()
                # print(data)
                if check_Amenities:
                    datas= Listing_Amenities.objects.filter(Amenities_ID__in =res ).values('listing_id')
                    print(datas)
                    id = []
                    for data in datas:
                        data = data['listing_id']
                        id.append(data)
                    queryset  =  listing.objects.filter(id__in=id)
            if check_Purpose_Type:
                queryset = queryset.filter(Purpose_Type=check_Purpose_Type)
            if check_Type:
                queryset = queryset.filter(Type=check_Type)
            if check_property_Type:
                queryset = queryset.filter(property__property_type=check_property_Type)
            if min_price == '':
                min_price = 0
            if min_price == '':
                queryset = queryset.all().aggregate(max('property_pricing'))
            if min_price and max_price:
                queryset = queryset.filter(property_pricing__range=(min_price,max_price))
            if check_property_size:
                queryset = queryset.filter(size=check_property_size)
            if check_bedroom:
                queryset = queryset.filter(Bedrooms=check_bedroom)
            if check_batroom:
                queryset = queryset.filter(Batrooms=check_batroom)
            if check_project_status:
                queryset = queryset.filter(Project_status=check_project_status)

            if not queryset:
                return Response({})

            return queryset
        except listing.DoesNotExist:
            raise Http404

class UpdateSlotsView(generics.UpdateAPIView):
    queryset = AvailableSlots.objects.all()
    serializer_class = SlotstSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)