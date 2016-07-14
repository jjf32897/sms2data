from django.shortcuts import render
from django.http import HttpResponse
import twilio.twiml

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

def hello(request):
    resp = twilio.twiml.Response()
    resp.message("what's up hello")
    return HttpResponse(str(resp))