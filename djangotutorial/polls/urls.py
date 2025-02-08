from django.urls import path

from .views import ProductsAPIView, ProductDetailAPIView, ShopsView, CategoriesView, BasketView, ContactView, \
    PartnerOrders, RegisterAccount, ConfirmAccount, AccountDetails, LoginAccount

app_name = 'polls'
urlpatterns = [
    path('products/', ProductsAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
    path('shops/', ShopsView.as_view()),
    path('basket/', BasketView.as_view(), name='basket'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('categories/', CategoriesView.as_view()),
]


#
# urlpatterns = [
#     path("", views.index, name="index"),
# ]