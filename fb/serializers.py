from rest_framework import serializers
from .models import FacebookUser
from rest_framework.reverse import reverse


class FBUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('user_info')
    pages = serializers.SerializerMethodField('page_list')

    def user_info(self, arg):
        return {"id": arg.user.id, "username": arg.user.username}

    def page_list(self, arg):
        resp = arg.pages
        return resp

    class Meta:
        model = FacebookUser
        fields = ('first_name', 'name', 'link', 'user', 'social_id', 'is_expired', 'pages', 'updated_at')
