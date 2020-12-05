from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import permissions, status


class TestView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        return Response('hello world', status=status.HTTP_200_OK)
