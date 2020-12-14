from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import APIView, api_view, throttle_classes, permission_classes
from rest_framework import permissions, status
from rest_framework.throttling import UserRateThrottle

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect


class TestRate(UserRateThrottle):
    rate = '1/day'


class TestView(APIView):
    """
        View to list all users in the system.

        * Requires token authentication.
        * Only admin users are able to access this view.
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request: Request):
        """
            Return a list of all users.
        """
        print(request.META['REMOTE_ADDR'])
        r = Response()
        r.data = 'hello mate'
        r.status_code = status.HTTP_200_OK
        r.delete_cookie('auth')
        return r


@api_view(['GET'])
def test2(request: Request):
    return redirect('test')