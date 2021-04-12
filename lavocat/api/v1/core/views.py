from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lavocat.api.v1.core import facade
from lavocat.api.v1.core.facade import UserNotAllowed, Unauthorized


class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            token_data = facade.google_auth(token)
            return Response(data=token_data)
        except (UserNotAllowed, Unauthorized):
            return HttpResponse(
                {'message': 'Não autorizado'}, status=status.HTTP_401_UNAUTHORIZED
            )
