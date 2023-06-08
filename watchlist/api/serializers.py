from rest_framework import serializers

from watchlist.models import WatchList, StreamPlatform, Review

# Model Serializer. They have inbuilt create/update methods

class ReviewSerializer(serializers.ModelSerializer):
    
    review_user = serializers.StringRelatedField(read_only = True) # To Display User's Name

    class Meta:
        model= Review
        exclude = ("watchlist", )


class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source = 'platform.name')

    class Meta:
        model= WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):

    watchlist = WatchListSerializer(many = True, read_only=True)

    
    class Meta:
        model= StreamPlatform
        fields = "__all__"
