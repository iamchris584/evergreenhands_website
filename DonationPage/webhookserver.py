import json
import os
import stripe
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from .models import Donation
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY



endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def webhook_request(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponseBadRequest('invalid payload')
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest('invalid signature')

    # check what happened 
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_intent_id = payment_intent['id']
        donation = Donation.objects.filter(stripe_payment_intent_id=payment_intent_id)
        print(f'my payment= {payment_intent_id}')
        if donation.exists():
            status = 'S'
            donation.update(status=status)
            try:
                donation=donation.first()
                context ={
                    'donor_name': donation.full_name, 
                    'amount': donation.amount,
                    'payment_intent_id': payment_intent_id,
                    'date': datetime.now().strftime("%B %d, %Y"),
                }
                html_output = render_to_string("main/email.html", context)
                text_string= strip_tags(html_output)
                email=EmailMultiAlternatives(
                    subject='Thank you for your donation',
                    body=text_string,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[donation.email],
                )
                email.attach_alternative(html_output, "text/html")
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Failed to dispatch donation receipt email for ID {payment_intent_id}: {e}")
        else:
            logger.warning(f"No donation record found matching Payment Intent: {payment_intent_id}")


    if event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        print('payment failed', payment_intent)
        payment_intent_id =payment_intent['id']
        donation = Donation.objects.filter(stripe_payment_intent_id=payment_intent_id)
        print(f'my payment= {payment_intent_id}')
        if donation.exists():
            status = 'F'
            donation.update(status=status)
        

    return HttpResponse(status=200)
