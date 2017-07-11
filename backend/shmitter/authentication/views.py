from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializers import JSONWebTokenSerializer


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username_or_email and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
