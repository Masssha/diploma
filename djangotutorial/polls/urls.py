from django.urls import path

from .views import ProductAPIView, PAPIView

app_name = 'polls'
urlpatterns = [
    path('product/', ProductAPIView.as_view()),
    path('p/', PAPIView.as_view())
]


#
# urlpatterns = [
#     path("", views.index, name="index"),
# ]