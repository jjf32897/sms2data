from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import twilio.twiml

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

@csrf_exempt
def hello(request):
	twiml = '<Response><Message>i said hey what\'s up hello</Message></Response>'
	return HttpResponse(twiml, content_type='text/xml')