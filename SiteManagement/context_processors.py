from SiteManagement.models import Footer

def base_view(request):
    return {
        'footer': Footer.objects.first()
    }