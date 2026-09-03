from django.shortcuts import render, redirect
from django.http import HttpResponse, request, JsonResponse

from .forms import DonationForm
from .models import Donation
import stripe
from stripe import PaymentIntent
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum



stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
# def donation_page(request):
#     return render(request, 'DonationPage/donation.html')


def form_fill(request):
    if request.method == 'POST':
        print("--- VIEW HAS BEEN HIT ---")
        form = DonationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # donor = form.cleaned_data['donor_name']
            # email = form.cleaned_data['email']
            # amount = form.cleaned_data['amount']
            # currency = form.cleaned_data['currency']
            # payment_method = form.cleaned_data['payment_method']
            # stripe_payment = form.cleaned_data['stripe_payment']
            # Donation.objects.create(donor_name=donor, email=email, amount=amount, currency=currency, payment_method=payment_method, stripe_payment=stripe_payment)
            donation = form.save()
            donor_id = donation.uuid
            
            print("Method:", request.method)
            print("Data:", request.POST)
            return redirect('card', pk=donor_id)
    else:
        
        form = DonationForm()
    return render(request, 'main/index.html', {'form':form})

@csrf_exempt
def card_payment(request, pk):
    # print(pk)
    donation_id = Donation.objects.get(uuid=pk)
    context = {}
    if donation_id.status == 'P':
        amount = donation_id.amount * 100
        currency = 'gbp'
        print(amount)
        stripe_intent= PaymentIntent.create(amount = amount, currency=currency, payment_method_types=['card'])
        Donation.objects.filter(id =donation_id.id).update(stripe_payment_intent_id=stripe_intent.id)
        context={'Secret': stripe_intent.client_secret}
        print('amount =', amount)
  
    return render(request, 'DonationPage/card.html', context)



def paymentSucess(request):
    return render(request, 'DonationPage/paymentSuccess.html')



# admin unfold cards to display models
def dashboard_callback(request, context):
    success = Donation.objects.filter(status='S').count()
    pending = Donation.objects.filter(status='P').count()
    donors = Donation.objects.all().count()
    total = Donation.objects.filter(status='S').aggregate(total=Sum('amount'))['total'] or 0
    recent_donations = Donation.objects.order_by("-created_date")[:5]
    context.update({
        "Successful" : success,
        "Pending" : pending,
        "donors" : donors,
        "total" : total,
        "recent_donations" : recent_donations,
        
    })
    return context