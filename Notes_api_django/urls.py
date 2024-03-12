"""
URL configuration for Notes_api_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import path, include
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns
from Notes_api_django import views
# from drf_yasg.views import get_schema_view  # pip install drf-yasg
# from drf_yasg import openapi

# Customizing the Swagger schema in get_schema_view() is important
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Notes_REST_API_Django",
#         default_version='v1',
#         description="API Description",
#         terms_of_service="https://www.app.com/terms/",
#         contact=openapi.Contact(email="contact.com"),
#         license=openapi.License(name="License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path("notes/", views.NoteList.as_view()),  # Defines the GET /notes/ endpoint
    path("notes/<int:pk>/", views.NoteDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),

    path("login/", views.login_view, name="api-login"),
    path("logout/", views.logout_view, name="api-logout"),
    path("register/", views.register_view, name="api-register"),
    path("whoami/", views.WhoAmIView.as_view(), name="api-whoami"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += [
#     path("api-auth/", include("rest_framework.urls")),
#     path('admin/', admin.site.urls),
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),  # regex
#             name='schema-json'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
#          name='schema-swagger-ui'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

# urlpatterns += [
#     path('admin/', admin.site.urls),
# ]
