from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import datetime


class ObtainExpiringAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            utc_now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
            if not created and token.created < utc_now - datetime.timedelta(hours=24):
                print("re-generate token for old one is expired")
                token.delete()
                token = Token.objects.create(user=user)
                token.created = datetime.datetime.utcnow()
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
