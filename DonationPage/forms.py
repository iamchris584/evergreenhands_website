from .models import Donation, ContactForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import re




class DonationForm(forms.ModelForm):
    privacy_consent = forms.BooleanField(
            required=True, 
            error_messages={'required': 'You must agree to our privacy policy.'}
            
        )
    class Meta:
        model = Donation
        exclude = ['created_date', 'status', 'stripe_payment_intent_id', 'uuid']

    def clean_full_name(self):
        # full_name = strip_tags(self.cleaned_data.get('full_name', '')).strip()
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 2:
            raise ValidationError("name too short must be atleast 2 characters long")
        if not re.match(r"^[A-Za-z\s'\-]+$", full_name):
            raise ValidationError("Name contains invalid characters or code tags.")
        return full_name

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise ValidationError('negative values not allowed')
        if amount < 10:
            raise ValidationError("not accepted")
        return amount
    def clean_email(self):
            email = self.cleaned_data.get('email', '').strip().lower()
            if re.search(r'[<>]', email):
                raise ValidationError("Invalid characters in email address.")
            return email

# class ContactUs(ModelForm):
#     class Meta:
#         model = ContactForm
#         exclude = ['created_at',]



class ContactUsForm(forms.ModelForm):
    contact_privacy_consent = forms.BooleanField(
        required=True, 
        error_messages={'required': 'You must agree to our privacy policy.'}
        
    )

    class Meta:
        model = ContactForm
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']

    def clean_first_name(self):
        first_name = strip_tags(self.cleaned_data.get('first_name', '').strip())
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters.")
        if not re.match(r"^[A-Za-z\s'\-]+$", first_name):
            raise ValidationError("First name contains invalid characters or code tags.")
        return first_name

    def clean_last_name(self):
        last_name = strip_tags(self.cleaned_data.get('last_name', '').strip())
        if len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters.")
        if not re.match(r"^[A-Za-z\s'\-]+$", last_name):
            raise ValidationError("Last name contains invalid characters or code tags.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if re.search(r'[<>]', email):
            raise ValidationError("Invalid characters in email address.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number') or ''
        phone = phone.strip()
        if phone:
            if not re.match(r"^\+?[0-9\s\-\(\)]{7,20}$", phone):
                raise ValidationError("Enter a valid phone number.")
        return phone

    def clean_message(self):
        raw_message = self.cleaned_data.get('message', '').strip()
        cleaned_message = strip_tags(raw_message)
        
        if re.search(r'[<>]', raw_message):
            raise ValidationError("HTML or code tags (< or >) are strictly prohibited.")
        if len(cleaned_message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return cleaned_message