from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

# Create your views here.

from .models import Evenement
from .forms import EvenementForm

def evenementen(request):
    template_name = 'evenementen/evenementen.html'
    evenement_list = Evenement.objects.all()
    context = {'evenement_list': evenement_list}
    return render(request, template_name, context)

def evenement_overzicht(request, slug):
    template_name = 'evenementen/evenement_overzicht.html'
    evenement = get_object_or_404(Evenement, slug=slug)
    context = {'evenement': evenement}
    return render(request, template_name, context)

@permission_required('evenementen.add_evenement')
def evenement_voegtoe(request):
    template_name = 'evenementen/evenement_voegtoe.html'
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save()
            return HttpResponseRedirect(reverse('evenementen:evenement_overzicht', args=[evenement.slug]))
    else:
        form = EvenementForm()
    context = {'form': form}
    return render(request, template_name, context)

@permission_required('evenementen.change_evenement')
def evenement_wijzig(request, slug):
    template_name = 'evenementen/evenement_wijzig.html'
    evenement = get_object_or_404(Evenement, slug=slug)
    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            evenement = form.save()
            return HttpResponseRedirect(reverse('evenementen:evenement_overzicht', args=[evenement.slug]))
    else:
        form = EvenementForm(instance=evenement)
    context = {'evenement': evenement, 'form': form}
    return render(request, template_name, context)
