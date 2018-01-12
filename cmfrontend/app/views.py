import os
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from app.forms import MomentForm,DiagonosForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import get_template
from app import models, forms
# Create your views here.
def welcome(request):
   template = get_template('welcome.html')
   html = template.render(locals)
   return HttpResponse(html)

def describe_input(request):
	if request.method == 'POST':
                form = MomentForm(request.POST)
                if form.is_valid():
                        moment = form.save()
                        moment.save()
                        return HttpResponseRedirect(reverse("app.views.welcome"))
	else:
                form = MomentForm()
	form = forms.MomentForm()
 	template = get_template('describe_input.html')
 	request_context = RequestContext(request)       
 	request_context.push(locals())
	html = template.render(request_context)
   
	return HttpResponse(html)


def diagonos_input(request):
        if request.method == 'POST':
                form = DiagonosForm(request.POST)
                if form.is_valid():
                        diagonos = form.save()
                        diagonos.save()
                        return HttpResponseRedirect(reverse("app.views.welcome"))
        else:
                form = DiagonosForm()
        form = forms.DiagonosForm()
        template = get_template('diagonos_input.html')
        request_context = RequestContext(request)
        request_context.push(locals())
        html = template.render(request_context)

        return HttpResponse(html)
