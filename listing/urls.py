from django.urls import path, include
from listing.views import *
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('get/', getallListing.as_view(), name='basic_view'),
    path('get/<int:pk>/', GetListingView.as_view(), name='basic_view'),
    path('post/', AddListingPostData.as_view(),name="post"),
    path('image/', ListMedia.as_view(),name='basic_view'),
    path('image/update/<int:pk>/', ListMediaUdate.as_view(),name="update_basic"),
    path('amenities/', AmenitiesView.as_view({"get": "list", "post": "create"}), name='basic_view'),
    path('amenities/update/<int:pk>/', UpdateAmenitiesView.as_view(), name="update_basic"),
    path('Listing_amenities/', ListingAmenitiesView.as_view({"get": "list", "post": "create"}), name='basic_view'),
    path('property/', FindProperty.as_view(),name="get_property"),
    path('filter/', filterView.as_view(),name="get_property"),
    path('mylisting/', MylistingView.as_view(),name="get_property"),
    
]
