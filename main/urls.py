from django.urls import path
from .views import index_view, mission_view, about_us, contact_us, send_message, privacy_policy, refund_policy, terms_of_services, projects_page, donation_page

urlpatterns = [
    path('', index_view, name="home"),
    path('Mission/', mission_view, name="mission"),
    path('AboutUs/', about_us, name='aboutus'),
    path('ContactUs/', contact_us, name="contactus"),
    path('send_message/', send_message, name="contact"),
    path('privacy/', privacy_policy, name="policy"),
    path('refund-policy/', refund_policy, name="refund-policy"),
    path('terms/', terms_of_services, name="terms"),
    path('projects/', projects_page, name="projects"),
    path('donation/', donation_page, name="giving"),
   

    
]
