from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
from sendsms import api

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

@twilio_view
def hello(request):
	if request.method == 'POST':
		# gets body of text, else None
		body = request.POST.get('Body', None)
		r = Response() # makes messages object

		if body is not None:
			r.message('The message you sent: ' + body)
		else:
			r.message('you didn\'t send anything...')

		return HttpResponse(r.toxml(), content_type='text/xml')
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')