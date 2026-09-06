from django.db import models

class HomePage(models.Model):
    # Added null=True to prevent database validation errors on existing null rows
    hero_text = models.CharField(max_length=800, blank=True, null=True)
    hero_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    mission_text = models.CharField(max_length=800, blank=True, null=True)
    mission_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    sickle_cell_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    poverty_relief_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    refugee_support_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    aboutus_text = models.CharField(max_length=200, blank=True, null=True)
    aboutus_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    get_in_touch_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Contents"

    def __str__(self):
        return 'Home Page Content'


class AboutUs(models.Model):
    aboutUs_subheading = models.CharField(max_length=800, blank=True, null=True)
    aboutUs_description = models.CharField(max_length=800, blank=True, null=True)
    aboutUs_banner_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    about_purpose_statement = models.CharField(max_length=300, blank=True, null=True)
    about_purpose_body = models.CharField(max_length=500, blank=True, null=True)
    aboutus_vision = models.CharField(max_length=500, blank=True, null=True)
    aboutus_vision_body = models.CharField(max_length=500, blank=True, null=True)
    aboutus_journey = models.CharField(max_length=500, blank=True, null=True)
    aboutus_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    class Meta:
        verbose_name = "About Us Content"
        verbose_name_plural = "About Us Content"

    def __str__(self):
        return 'About Us'


class Our_Mission(models.Model):
    mission_hero_description = models.CharField(max_length=500, blank=True, null=True)
    mission_statement = models.CharField(max_length=500, blank=True, null=True)
    mission_vision = models.CharField(max_length=500, blank=True, null=True)
    mission_gallery_image1 = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    mission_gallery_image2 = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    mission_gallery_image3 = models.ImageField(upload_to='site_settings/', blank=True, null=True)

    class Meta:
        verbose_name = "Our Mission Content"
        verbose_name_plural = "Our Mission Content"

    def __str__(self):
        return 'Our Mission'


class Footer(models.Model):
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Footer & Contact Info"
        verbose_name_plural = "Footer & Contact Info"

    def __str__(self):
        return "Footer Settings"


