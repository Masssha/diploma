from django.urls import path

from .views import ProductsAPIView, ProductDetailAPIView, ShopsView, CategoriesView, BasketView

app_name = 'polls'
urlpatterns = [
    path('products/', ProductsAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
    path('shops/', ShopsView.as_view()),
    path('basket/', BasketView.as_view(), name='basket'),
    path('categories/', CategoriesView.as_view()),
]


#
# urlpatterns = [
#     path("", views.index, name="index"),
# ]