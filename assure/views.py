from django.shortcuts import get_object_or_404, render
from .models import Site, Pilot, Comment
from django.template import loader
import code

def index(request):
    latest_site_list = Site.objects.order_by('-pub_date')[:5]
    template = loader.get_template('assure/index.html')
    context = { 'latest_site_list':latest_site_list }
    #code.interact(local=dict(globals(), **locals()))
    return render(request, 'assure/index.html', context)

def detail(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    return render(request, 'assure/detail.html', {'site': site})

def results(request, site_id):
    response = "You're looking at the results of the site %s."
    return HttpResponse(response % site_id)

def comment(request, site_id):
    return HttpResponse("You're commenting on the pilot test for %s." % site_id)
