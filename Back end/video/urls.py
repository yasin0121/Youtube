from django.urls import path
from api.views import home_video,update_video


app_name = "video"


urlpatterns = [
    path("videos/", home_video, name="home"),
    path("video/<id>/", update_video, name="update_video"),

    # path('<uuid:uuid>', details_video, name="details_video"),
]
