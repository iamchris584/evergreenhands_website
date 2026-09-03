from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Donation, ContactForm, Projects, TeamMemeber



# Register your models here.

# admin.site.register(Donation)

@admin.register(Donation)
class Donationadmin(ModelAdmin):
    list_display = ['id', "full_name", "email", "stripe_payment_intent_id", "amount", "status", "created_date", "uuid"]


@admin.register(ContactForm)
class ContactFormAdmin(ModelAdmin):
    list_display = ['id', "first_name", "last_name", "email", "phone_number", "message", "created_date"]



@admin.register(Projects)
class ProjectsAdmin(ModelAdmin):
    list_display = [
    'title',
    'description',
    'image',
    'order',
    'created_at',
    'updated_at',
    'status',
    'date_label',
    'scheduled_date',
    'read_time',
    'created_at',
    'updated_at'
]


@admin.register(TeamMemeber)
class TeamMemberAdmin(ModelAdmin):
    list_display = ['full_name', 'image', 'role']







# project/urls.py or app/admin.py
from django.contrib import admin

# Change the main banner header text ("Django administration")
admin.site.site_header = "Evergreen Hands Admin"

# Change the browser tab title
admin.site.site_title = "Evergreen Hands Portal"

# Change the title on the admin home page index
admin.site.index_title = "Welcome to the Operations Portal"