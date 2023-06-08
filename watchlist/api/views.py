from watchlist.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from django.contrib.auth.models import User
# For functon basd>
# from rest_framework.decorators import api_view

# For Class basd>
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

# Custom permissions
from watchlist.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

# Filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist.api.pagination import WatchListPageNumberPagination,WatchListLOPagination,WatchListCPagination

############# USE PATCH REQUEST FOR PARTIAL UPDATES #############




# Working on Filtering
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # username = self.kwargs['username']
        username = self.request.query_params.get('username', None)

        # Jump to the FK provided & check the username param as lookup
        # in the FK object provided.
        # Filtering by user, URL.
        # return Review.objects.filter(review_user__username = username)
        return Review.objects.filter(review_user__username = username)
        






'''
Using Concrete View Classes

ListCreateAPIView = Supports creation & Selection
RetrieveUpdateDestroyAPIView = Supports Selection(get-pk), updation & Destroy.
'''

class ReviewCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    '''
    Here, to update or write a movie reviw, 
    1. get the movie using id
    2. since we alredy know for which movie we are reviewing, there
          is no need to enter WATCHLIST FIELD MANUALLY
    3. So excude the WATCHLIST FIELD in serializer, as the POST request no
        more contains WATCLIST FIELD
    4. WATCHLIST will be updated automatically by mentioning them in serializer.save()
    5. the movie objct retrieved earlier will be connected to the WATCHLIST filed of review class
        so that the new reviews are for that same Movie.
    '''
    serializer_class = ReviewSerializer

    # For 1time Create Review function.
    def get_queryset(self):
        return Review.objects.all()
    

    def perform_create(self, serializer): 
        pk = self.kwargs.get('pk')
        retrieved_movie = WatchList.objects.get(pk = pk)

        # Allowing only 1 review for a movie by a user.

        review_user = self.request.user
        if Review.objects.filter(watchlist = retrieved_movie, review_user = review_user).exists():
            raise ValidationError("You have already reviewed this movie")

        
        # Calculate the avg_review & Total no. of ratings for the movie
        '''
        Remember: Generics used to di direct create, 
        creation and update along with custom calculation must be
        separately done.

        To Perfrom custome calculation, follow below steps::>>
        '''
        if retrieved_movie.number_rating == 0:
            retrieved_movie.avg_rating = serializer.validated_data['rating']
        else:
            retrieved_movie.avg_rating= ( retrieved_movie.avg_rating + serializer.validated_data['rating'])/2

        retrieved_movie.number_rating +=1
        retrieved_movie.save()

        serializer.save(watchlist = retrieved_movie, review_user = review_user)



class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [filters.SearchFilter]
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # filter_backends = [filters.OrderingFilter]
    # filterset_fields =['title', 'platform__name']
    # search_fields =['^title', '=platform__name'] # '=' : Exact Match like Filter
    # ordering_fields =['-avg_rating'] # '-' : Reverse Ordering

    # pagination_class = WatchListPageNumberPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination
    
   





class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend] # Which Filter to apply to the backend
    filterset_fields = ['review_user__username','active'] # Where to apply filter


    def get_queryset(self):
        pk= self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformListAV(APIView):

    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        streamers = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamers, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self , request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):

    permission_classes = [AdminOrReadOnly]


    def get(self, request,pk):
        streamers = StreamPlatform.objects.get(id=pk)
        serializer = StreamPlatformSerializer(streamers, context={'request':request})
        return Response(serializer.data)
    
    def put(self , request,pk):
        streamers = StreamPlatform.objects.get(id=pk)
        serializer = StreamPlatformSerializer(streamers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk):
        streamers = StreamPlatform.objects.get(id=pk)
        streamers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):

    permission_classes = [AdminOrReadOnly]
   
    def get(self,  request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WatchListDetailAV(APIView):

    permission_classes = [AdminOrReadOnly]

   
    def get(self,  request, pk):
        try:
            movie_instance = WatchList.objects.get(id=pk)
            serializer = WatchListSerializer(movie_instance)
            return Response(serializer.data)

        except WatchList.DoesNotExist: ## Trick in Script
            return Response({'Error':'Item Doesnt Exist'},status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        movie = WatchList.objects.get(id=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        WatchList.objects.get(id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

