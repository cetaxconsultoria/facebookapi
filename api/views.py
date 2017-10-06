from rest_framework.views import APIView
from rest_framework.response import Response
from fb.serializers import FBUserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from fb.models import FacebookUser
from fb.facebook_methods import get_graph
from rest_framework import generics
from rest_framework import filters
from rest_condition import Or
from .roles import IsFreeUser, IsPayingUser
from rest_framework.reverse import reverse

# Create your views here.


class UserList(generics.ListAPIView):
    """
        Lista de Spotteds aprovados pela moderação e pela API.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = [Or(IsAdminUser, IsPayingUser), ]
    queryset = FacebookUser.objects.all()
    serializer_class = FBUserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    throttle_classes = (ScopedRateThrottle,)
    # throttle_scope = 'list'
    filter_fields = ('id')
    # search_fields = ('message', 'suggestion')
    # ordering_fields = ('message', 'by_api', 'id', 'created', 'suggestion')


class PageInfo(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = [Or(IsAdminUser, IsPayingUser, IsFreeUser, IsAuthenticated), ]
    throttle_classes = (ScopedRateThrottle,)

    def get(self, request):
        content = {
            'page_id': request.GET['id'],
        }
        response = get_graph().get_object(content['page_id'] + "?fields=posts{likes{name},comments,message}")
        return Response(response)
