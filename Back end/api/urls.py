from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import home_video,update_video

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/video/", home_video, name="home"),
    path("api/video/<id>/", update_video, name="update_video"),
]