from rest_framework import generics
from user.serializer import UserSerializer


# CreateAPIView handles post request that are designed for creating objects
# as we have defined serializer inside view class therefore it will know which model to use
# when we make HTTP request it goes through the URL and it is passed into CreateAPIView class which will call the serializer and create the objects and return appropriate response
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
