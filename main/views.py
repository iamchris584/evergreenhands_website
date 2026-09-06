from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from DonationPage.forms import ContactUsForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from DonationPage.models import Projects, TeamMemeber
from SiteManagement.models import HomePage, AboutUs,  Our_Mission, Footer


# Create your views here.
def index_view(request):
    recent = Projects.objects.order_by('-created_at')[:3]
    home_page = HomePage.objects.all().first()
    context = { 'projects' : recent, 'home_page':home_page}
    return render(request, 'main/index.html', context)

def mission_view(request):
    founders = TeamMemeber.objects.all()
    mission = Our_Mission.objects.all().first()
    context = {'founders': founders, 'mission':mission}
    return render(request, 'main/mission.html', context)


def about_us(request):
    about = AboutUs.objects.all().first()
    context = {'about':about}
    return render(request, 'main/aboutus.html', context)

def contact_us(request):
    footer = Footer.objects.all().first()
    context = {'footer':footer}
    return render(request, 'main/contactus.html', context)

def privacy_policy(request):
    return render(request, 'main/privacy.html')

def refund_policy(request):
    return render(request, 'main/refund-policy.html')

def terms_of_services(request):
    return render(request, 'main/terms_of_service.html')

def projects_page(request):
    projects = Projects.objects.all()
    print(projects)
    context = { 'projects' : projects}
    return render(request, 'main/projects.html', context)

def donation_page(request):
    return render(request, 'main/donationpage.html')





def send_message(request):
    if request.method == 'POST':
        print("--- VIEW HAS BEEN HIT ---")
        form = ContactUsForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            email_from = form.cleaned_data.get('email')
            form.save()
            email = EmailMessage(
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[email_from],

            )
            email.send(fail_silently=False)
          
            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully!'
            })
            

        else:
            # Returns Django's field validation errors (e.g. {'first_name': ['First name must be at least 2 characters.']})
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    else:
        form = ContactUsForm()
    return render(request, 'main/index.html', {'form':form})