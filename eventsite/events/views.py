# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from datetime import datetime

# Django
from django.shortcuts import render
from django.contrib.auth.models import User

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

# Provider OAuth2
from provider.oauth2.models import Client

# Event App
from events.serializers import RegistrationSerializer
from events.serializers import UserSerializer, EventSerializer
from events.models import Event

class RegistrationView(APIView):
    # Allow registration of new users
    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data = request.DATA)

        # Check format and unique constraint
        if not serializer.is_valid():
            return Response(serializer.errors, \
                            status = status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        user = User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()

        # Create OAuth2 client
        name = user.username
        client = Client(user=user, name=name, url='' + name,\
                client_id=name, client_secret='', client_type=1)
        client.save()

        return Response(serializer.data, \
                        status=status.HTTP_201_CREATED)

class EventsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        # Get all events
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Adding a new events
        serializer = EventSerializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors, \
                            status = status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            event = Event(owner = owner,
                          description = data['description'],
                          date = data['date'],
                          location = data['location'],
                          tags = data['tags'],
                          title = data['title'],
                          link = data['link'],
            )
            event.save()
            request.DATA['id'] = event.pk
            return Response(request.DATA, status = status.HTTP_201_CREATED)

    def put(self, request, event_id):
        # update an event
        serializer = EventSerializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors, \
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            event = Event(id = event_id,
                          owner = request.user,
                          description = data['description'],
                          date = data['date'],
                          location = data['location'],
                          tags = data['tags'],
                          title = data['title'],
                          link = data['link'],
            )
            event.save()
            return Response(request.DATA, status = status.HTTP_200_OK)


def defaultAll(request):

    eventList = Event.objects.all()
    print eventList
    return render_to_response('index.html',{'events': eventList})










