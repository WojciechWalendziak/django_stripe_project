from django.urls import path
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('add/', BookCreateView.as_view(), name='add'),
    path('logout/', logout_request, name='logout'),
    path('detail/<id>/', BookDetailView.as_view(), name='detail'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),
    path('config/', stripe_config),
    path('create-checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
]