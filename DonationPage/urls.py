from django.urls import path
from .views import  form_fill, card_payment, paymentSucess
from .webhookserver import webhook_request

urlpatterns = [
    # path('donate/', donation_page, name='donation'),
    path('donate2/', form_fill, name='donation'),
    path('card/<uuid:pk>', card_payment, name='card'),
    path('payout/', webhook_request, name='payout'),
    path('success/', paymentSucess, name='paymentSucessful'),

]