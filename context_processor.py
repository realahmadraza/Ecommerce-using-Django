from homeshop.models import Footerinfo, About
from django.shortcuts import render


def footer_info(request):
    footer_info = Footerinfo.objects.all()
    short_about = Footerinfo.objects.values_list('short_About', flat=True).first()
    return {
        'footer_info': footer_info,
        'short_about': short_about,
    }

def about_info(request):
    about_info = About.objects.all()
    context = {
        'about_info': about_info,
    }
    return render(request, 'homeshop/about-us.html', context)