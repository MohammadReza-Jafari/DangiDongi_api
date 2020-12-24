from rest_framework import generics, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from .serializers import CreateGroupSerializer, GroupListSerializer


class CreateGroupView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @swagger_auto_schema(
        request_body=CreateGroupSerializer,
        operation_description="ساخت گروه جدید\n\n"
                              "token needed\n * pattern is 'Bearer token-value' in header",
        responses={
            status.HTTP_201_CREATED: "create group is successful",
            status.HTTP_400_BAD_REQUEST: 'something is wrong'
        }
    )
    def post(self, request:Request):
        ser = CreateGroupSerializer(data=request.data)

        if ser.is_valid():
            group = ser.save(admin=request.user)
            group.members.add(request.user)

            response = {
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'گروه با موفقیت ساخته شد',
                'data': ser.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class GetGroupsView(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupListSerializer

    def get_queryset(self):
        return self.request.user.teams
