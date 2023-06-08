from django.urls import path, include
from watchlist.api.views import (WatchListAV,WatchListDetailAV, 
                                 StreamPlatformListAV,StreamPlatformDetailAV, 
                                 ReviewList, ReviewDetail, ReviewCreate, UserReview, 
                                 WatchListGV)

urlpatterns = [

    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-detail'),
    path('streamers/list/', StreamPlatformListAV.as_view(), name='streamer-list'),
                            # name attribute as per HyperlinkedModelSerializer
    path('streamer/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    # URL For Filtering
    # path('reviews/<str:username>/',UserReview.as_view(),name='user-review-detail')
    path('reviews/',UserReview.as_view(),name='user-review-detail')

]
