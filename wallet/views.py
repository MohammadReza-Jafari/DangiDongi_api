from rest_framework import status, permissions, generics, pagination, filters
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import APIView


from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from .serializers import WalletSerializer


class ChargeWalletView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    @swagger_auto_schema(
        request_body=WalletSerializer,
        operation_description='شارژ کیف پول\n\n'
                              "token needed\n * pattern is 'Bearer token-value' in header",
        responses={
            status.HTTP_400_BAD_REQUEST: 'something is wrong.',
            status.HTTP_403_FORBIDDEN: 'authentication error',
            status.HTTP_200_OK: 'every thing is okay'
        }
    )
    def post(self, request: Request):
        ser = WalletSerializer(data=request.data)

        if ser.is_valid():
            user = request.user
            user.wallet.amount += ser.validated_data.get('amount', None)
            user.wallet.save()

            response = {
                'success': True,
                'message': 'شارژ با موفقیت انجام شد',
                'amount': user.wallet.amount,
                'status': status.HTTP_200_OK
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


