"""
All the views related to citizen and custom api for Paranuara views are present here.
"""
from django.shortcuts import get_list_or_404
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from citizen.models import Citizen, Friend
from citizen.serializer import CitizenSerializer, FriendSerializer, CitizenSerializersWithoutFriend, \
    FavouriteFoodSerializer, CitizenFriendsSerializer
from company.models import Companies


class CitizenViewset(viewsets.ModelViewSet):
    """
    This viewset provides all the basic functionality like get, put and
    post for the Citizen model.
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Citizen.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = CitizenSerializer


class FriendViewset(viewsets.ModelViewSet):
    """
    This viewset provides all the basic functionality like get, put and
    post for the Friend model.
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Friend.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = FriendSerializer


class ParanuaraViewset(viewsets.ModelViewSet):
    """
    This viewset provides all the custom api definitions as per business
    requirements.
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Citizen.objects.all()

    serializer_class = CitizenSerializer
    pagination_class = None

    def search_employee(self, request, *args, **kwargs):
        """
        Given a company, the API needs to return all their employees.
        Provide the appropriate solution if the company does not have any employees.

        :param request: django wrapper for the request use in case of post request.
        :param args: args
        :param kwargs: Kwargs from the get URL
        :return: Response object meeting the requirements.
        """
        try:
            keyword = kwargs['keyword']
            if Companies.__dict__.get(keyword, ''):
                match = kwargs['match']
                keyword_str = f"company_id__{keyword}__iexact"
                queryset = Citizen.objects.filter(
                    **{keyword_str: match}).all()
                dataset = get_list_or_404(queryset)
                return Response(
                    CitizenSerializersWithoutFriend(each_object).data for each_object in
                    dataset)
            else:
                return Response(
                    {"Error": f"Citizen does not have {keyword} parameter"})
        except Exception as error:
            return Response({"Failure": f"Unable to serve this request. Error occured {error} ... "})

    def get_favourites(self, request, *args, **kwargs):
        """
         Given 1 people, provide a list of fruits and vegetables they like.
         This endpoint must respect this interface for the output:
         `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

        :param request: django wrapper for the request use in case of post request.
        :param args: args
        :param kwargs: Kwargs from the get URL
        :return: Response object meeting the requirements.
        """
        try:
            keyword = kwargs['keyword']
            if Citizen.__dict__.get(keyword, ''):
                match = kwargs['match']
                keyword_str = f"{keyword}__iexact"
                queryset = Citizen.objects.filter(
                    **{keyword_str: match}).all()
                dataset = get_list_or_404(queryset)
                return Response(
                    FavouriteFoodSerializer(each_object).data for each_object in
                    dataset)
            else:
                return Response(
                    {"Error": f"Citizen does not have {keyword} parameter"})
        except Exception as error:
            return Response({"Failure": f"Unable to serve this request. Error occured {error} ... "})

    def find_friends(self, request, *args, **kwargs):
        """
        Given 2 people, provide their information (Name, Age, Address, phone) and the list
        of their friends in common which have brown eyes and are still alive.

        :param request: django wrapper for the request use in case of post request.
        :param args: args
        :param kwargs: Kwargs from the get URL
        :return: Response object meeting the requirements.
        """
        try:

            keyword = kwargs['keyword']
            if Citizen.__dict__.get(keyword, ''):
                friends = kwargs['match'].split(',')
                if len(friends) != 2:
                    return Response(
                        {"Failure": f"This api can be used only when 2 friend are provied, but provided {friends} "})

                keyword_str = f"{keyword}__in"
                queryset = Citizen.objects.filter(
                    **{keyword_str: friends}).all()
                dataset = get_list_or_404(queryset)
                if len(dataset) != 2:
                    return Response({"Failure": f" At least one citizen missing {friends} "})

                friendset1 = {friend_data.pop('index'): friend_data for friend in
                              CitizenFriendsSerializer(dataset[0]).data['annotated_relationships'] for friend_data in
                              friend.values()}
                friendset2 = {friend_data.pop('index'): friend_data for friend in
                              CitizenFriendsSerializer(dataset[1]).data['annotated_relationships'] for friend_data in
                              friend.values()}

                common_friends = set(friendset1.keys()).intersection(set(friendset2.keys()))

                acceptable_friends = []
                for each in common_friends:
                    friend = friendset1.get(each)
                    if friend.pop('eye_color') == 'brown' and not friend.pop('has_died'):
                        acceptable_friends.append(friend)

                return Response(acceptable_friends)
            else:
                return Response(
                    {"Error": f"Citizen does not have {keyword} parameter"})
        except Exception as error:
            return Response({"Failure": f"Unable to serve this request. Error occured {error} ... "})
