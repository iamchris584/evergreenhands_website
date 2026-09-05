import logging
import requests
import json
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from .models import Donation


logger = logging.getLogger(__name__)


@csrf_exempt
def webhook_request(request):

    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    print("SUMUP WEBHOOK:", data)

    event_type = data.get('event_type')
    checkout_id = data.get('id')

    if event_type != 'CHECKOUT_STATUS_CHANGED':
        # SumUp may introduce other events in the future.
        # We simply acknowledge events we don't currently handle.
        return HttpResponse(status=200)

    if not checkout_id:
        return HttpResponseBadRequest("Missing checkout ID")

    # Find our donation using the SumUp checkout ID
    donation = Donation.objects.filter(
        sumup_checkout_id=checkout_id
    ).first()

    if not donation:
        logger.warning(
            f"No donation found for SumUp checkout {checkout_id}"
        )

        # Still return 200 so SumUp doesn't keep retrying
        return HttpResponse(status=200)

    # Verify the checkout directly with SumUp
    headers = {
        "Authorization": f"Bearer {settings.SUMUP_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            f"https://api.sumup.com/v0.1/checkouts/{checkout_id}",
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        checkout = response.json()

    except requests.RequestException as e:
        logger.error(
            f"Failed to verify SumUp checkout "
            f"{checkout_id}: {e}"
        )

        # Return non-2xx so SumUp can retry
        return HttpResponse(
            "Unable to verify checkout",
            status=500
        )

    checkout_status = checkout.get('status')

    print(
        f"SumUp checkout {checkout_id} status: "
        f"{checkout_status}"
    )

    # =========================
    # SUCCESSFUL PAYMENT
    # =========================

    if checkout_status == 'PAID':

        # Idempotency:
        # If this webhook arrives again, don't send
        # another receipt email.
        if donation.status == 'S':
            return HttpResponse(status=200)

        donation.status = 'S'
        donation.save(
            update_fields=['status']
        )
        print("PAYMENT IS PAID — ABOUT TO SEND EMAIL")
        try:
            context = {
                'donor_name': donation.full_name,
                'amount': donation.amount,
                'checkout_id': checkout_id,
                'date': datetime.now().strftime(
                    "%B %d, %Y"
                ),
            }

            html_output = render_to_string(
                "main/email.html",
                context
            )

            text_string = strip_tags(html_output)

            email = EmailMultiAlternatives(
                subject='Thank you for your donation',
                body=text_string,
                from_email=settings.EMAIL_HOST_USER,
                to=[donation.email],
            )

            email.attach_alternative(
                html_output,
                "text/html"
            )

            email.send(
                fail_silently=False
            )

        except Exception as e:
            logger.error(
                f"Failed to send donation receipt "
                f"for checkout {checkout_id}: {e}"
            )

    # =========================
    # FAILED PAYMENT
    # =========================

    elif checkout_status == 'FAILED':

        donation.status = 'F'
        donation.save(
            update_fields=['status']
        )

    # =========================
    # EXPIRED PAYMENT
    # =========================

    elif checkout_status == 'EXPIRED':

        donation.status = 'F'
        donation.save(
            update_fields=['status']
        )

    return HttpResponse(status=200)