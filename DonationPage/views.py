from django.shortcuts import render, redirect
from django.http import HttpResponse, request, JsonResponse

from .forms import DonationForm
from .models import Donation
# import stripe
# from stripe import PaymentIntent
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import requests



# stripe.api_key = settings.STRIPE_SECRET_KEY

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


def payment_choice(request, pk):
    donation = get_object_or_404(Donation, uuid=pk)

    return render(
        request,
        'DonationPage/card.html',
        {'donation': donation}
    )
# @csrf_exempt
# def card_payment(request, pk):
#     # print(pk)
#     donation_id = Donation.objects.get(uuid=pk)
#     context = {}
#     if donation_id.status == 'P':
#         amount = donation_id.amount * 100
#         currency = 'gbp'
#         print(amount)
#         stripe_intent= PaymentIntent.create(amount = amount, currency=currency, payment_method_types=['card'])
#         Donation.objects.filter(id =donation_id.id).update(stripe_payment_intent_id=stripe_intent.id)
#         context={'Secret': stripe_intent.client_secret}
#         print('amount =', amount)
  
#     return render(request, 'DonationPage/card.html', context)

# the main view
@csrf_exempt
def card_payment(request, pk):
    donation = get_object_or_404(Donation, uuid=pk)

    if donation.status != 'P':
        return redirect('paymentSucessful')

    checkout_data = {
        "checkout_reference": str(donation.uuid),
        "amount": float(donation.amount),
        "currency": "GBP",
        "merchant_code": settings.SUMUP_MERCHANT_CODE,
        "description": "Donation to Evergreen Hands",
        "hosted_checkout": {
            "enabled": True
        },
        "redirect_url": "https://evergreenhands.org/",
        "return_url": "https://evergreenhands.org/donate/payout/",
    }

    headers = {
        "Authorization": f"Bearer {settings.SUMUP_API_KEY}",
        "Content-Type": "application/json",
    }
    

    try:
        response = requests.post(
            "https://api.sumup.com/v0.1/checkouts",
            json=checkout_data,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        checkout = response.json()

        checkout_id = checkout.get("id")
        hosted_checkout_url = checkout.get("hosted_checkout_url")

        if not checkout_id or not hosted_checkout_url:
            print("Unexpected SumUp response:", checkout)
            return HttpResponse(
                "Unable to create payment checkout.",
                status=500,
            )

        donation.sumup_checkout_id = checkout_id
        donation.save(update_fields=["sumup_checkout_id"])

        return redirect(hosted_checkout_url)

    except requests.RequestException as e:
        print("SumUp API error:", e)

        return HttpResponse(
            "Unable to connect to the payment provider.",
            status=502,
        )

# @csrf_exempt
# def card_payment(request, pk):
#     donation = get_object_or_404(Donation, uuid=pk)

#     if donation.status != 'P':
#         return redirect('paymentSucessful')

#     context = {
#         'donation': donation,
#     }

#     return render(request, 'DonationPage/card.html', context)


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