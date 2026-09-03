from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminImageFieldWidget, UnfoldAdminTextareaWidget
from SiteManagement.models import AboutUs, Footer, Our_Mission, HomePage


@admin.register(HomePage)
class HomePageAdmin(ModelAdmin):
    list_display = ('id', 'hero_text', 'mission_text', 'aboutus_text')
    list_display_links = ('id', 'hero_text')

    formfield_overrides = {
        models.ImageField: {"widget": UnfoldAdminImageFieldWidget},
    }

    fieldsets = (
        ("Hero Banner", {
            "fields": ("hero_text", "hero_image"),
        }),
        ("Mission Preview", {
            "fields": ("mission_text", "mission_image"),
        }),
        ("Cause Images", {
            "fields": (
                "sickle_cell_image",
                "poverty_relief_image",
                "refugee_support_image",
            ),
        }),
        ("About Us Section", {
            "fields": ("aboutus_text",),
        }),
    )


@admin.register(AboutUs)
class AboutUsAdmin(ModelAdmin):
    list_display = ('id', 'aboutUs_subheading', 'about_purpose_statement', 'aboutus_vision')
    list_display_links = ('id', 'aboutUs_subheading')

    formfield_overrides = {
        models.ImageField: {"widget": UnfoldAdminImageFieldWidget},
    }


@admin.register(Our_Mission)
class Our_MissionAdmin(ModelAdmin):
    list_display = ('id', 'mission_statement', 'mission_vision')

    formfield_overrides = {
        models.ImageField: {"widget": UnfoldAdminImageFieldWidget},
    }


@admin.register(Footer)
class FooterAdmin(ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'address')
    list_display_links = ('id', 'email')