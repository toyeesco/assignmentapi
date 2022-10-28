from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import UserCreationSerializer, LogoutSerializer, ProfileSerializer, LocationSerializer, UserListSerializer
from .models import User
# Create your views here.



class UserCreationView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer


    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, format=None):
    #     user = User.objects.all()
    #     serializer = UserCreationSerializer(user,many=True)
    #     return Response(serializer.data)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

class ListLocationUsers(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = User.objects.all()

class ListAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()

         return Response(status=status.HTTP_204_NO_CONTENT)