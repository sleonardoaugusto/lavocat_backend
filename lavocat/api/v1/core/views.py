from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lavocat.api.v1.core import facade
from lavocat.api.v1.core.facade import UserNotAllowed, Unauthorized
from lavocat.api.v1.core.serializers import GoogleAuthSerializer


class GoogleAuthViewset(viewsets.ViewSet):
    serializer_class = GoogleAuthSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token_data = facade.google_auth(serializer.data['token'])
            return Response(data=token_data)
        except (UserNotAllowed, Unauthorized):
            return Response(
                {'message': 'Não autorizado'}, status=status.HTTP_401_UNAUTHORIZED
            )
