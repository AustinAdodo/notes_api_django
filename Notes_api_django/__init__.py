import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from models import Note
from serializers import NoteSerializer, UserSerializer
from permissions import IsOwnerOrReadOnly


class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = IsAuthenticated, IsOwnerOrReadOnly,


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@require_POST
def register_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username:
        return JsonResponse({"message": "no username provided"}, status=422)
    elif not password:
        return JsonResponse({"message": "no password provided"}, status=422)

    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError as e:
        return JsonResponse({"message": str(e)}, status=401)

    login(request, user)
    return JsonResponse({"message": "successfully registered"})


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username:
        return JsonResponse({"message": "no username provided"}, status=422)
    elif not password:
        return JsonResponse({"message": "no password provided"}, status=422)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"message": "invalid credentials"}, status=401)

    login(request, user)
    return JsonResponse({"message": "logged in"})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "not logged in"}, status=401)

    logout(request)
    return JsonResponse({"message": "logged out"})


class WhoAmIView(APIView):
    authentication_classes = SessionAuthentication, BasicAuthentication
    permission_classes = IsAuthenticated,

    @staticmethod
    def get(request, format=None):
        return JsonResponse({"username": request.user.username})

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
