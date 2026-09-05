from django.urls import path
from .views import  form_fill, card_payment, paymentSucess, payment_choice
from .webhookserver import webhook_request

urlpatterns = [
    # path('donate/', donation_page, name='donation'),
    path('donate2/', form_fill, name='donation'),
    path('card/<uuid:pk>/', payment_choice, name='card'),
    path('card/pay/<uuid:pk>/', card_payment, name='card_payment'),
    path('payout/', webhook_request, name='payout'),
    path('success/', paymentSucess, name='paymentSucessful'),

]