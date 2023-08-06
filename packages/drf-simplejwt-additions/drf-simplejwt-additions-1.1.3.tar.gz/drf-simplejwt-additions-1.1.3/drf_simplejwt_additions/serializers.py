from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class TokenObtainPairWithFullUserSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = {}
        fields = (i.name for i in User._meta.fields if i.name != 'last_login')
        for field in fields:
            user_data[field] = str(getattr(user, field))
        token['user'] = user_data
        token['sub'] = user_data['username']
        return token
