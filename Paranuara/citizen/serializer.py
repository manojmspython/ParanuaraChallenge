"""
The Different Serializers for Citizen and Friend are provided here.
"""
from rest_framework import serializers

from citizen.models import Citizen, Friend
from company.serializer import CompaniesSerializer


class CitizenSerializersWithoutFriend(serializers.ModelSerializer):
    """
    Serializes every attribute in Citizen other than the friendship.
    """
    company_id = CompaniesSerializer(required=False)
    friend = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=1000)
    )
    fruits = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    vegetables = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )

    class Meta:
        model = Citizen
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    """
    Serializes Friend model with only considering the To friend
    where my definition of friend is From ----> To Friend
    """
    friend_index = CitizenSerializersWithoutFriend()

    class Meta:
        model = Friend
        fields = ['friend_index']


class CitizenSerializer(serializers.ModelSerializer):
    """
    Serializes every attribute in Citizen model
    """
    company_id = CompaniesSerializer()
    friend = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=1000)
    )
    fruits = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    vegetables = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    annotated_relationships = FriendSerializer(source='get_relations', many=True)

    class Meta:
        model = Citizen

        fields = [field.name for field in model._meta.fields] + ['annotated_relationships']


class FavouriteFoodSerializer(serializers.ModelSerializer):
    """
    This Serializer is used when the favourite fruit and vegetable
    details of citizen needs to displayed or exported.
    """
    username = serializers.CharField(source='name')
    fruits = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )
    vegetables = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )

    class Meta:
        model = Citizen

        fields = ['username', 'age', 'fruits', 'vegetables']


class CommonCitizenSerializer(serializers.ModelSerializer):
    """
    Serializer for citizen model.
    """

    class Meta:
        model = Citizen
        fields = ['name', 'age', 'address', 'phone', 'has_died', 'eye_color', 'index']


class CommonFriendSerializer(serializers.ModelSerializer):
    """
    Serializer for Friend model.
    """
    friend_index = CommonCitizenSerializer()

    class Meta:
        model = Friend
        fields = ['friend_index']


class CitizenFriendsSerializer(serializers.ModelSerializer):
    """
    Serializer for citizen model which stores only the details of friends.
    """
    annotated_relationships = CommonFriendSerializer(source='get_relations', many=True)

    class Meta:
        model = Citizen

        fields = ['annotated_relationships']
