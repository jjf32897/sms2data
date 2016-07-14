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
	# if POSTed to by twilio...
	if request.method == 'POST':
		# gets body of text, else None
		body = request.POST.get('Body', None)
		number = request.POST.get('From', None)

		# api.send_sms(body='The message you sent: ' + body, from_phone='+13098086245', to=['+1' + number])
		
		# twilio response
		r = Response() # makes messages object

		if body is not None:
			r.message('The message you sent: ' + body + "; Your digits: " + number)
		else:
			r.message('Error')

		return HttpResponse(r.toxml(), content_type='text/xml')

	# if accessing the webpage via GET
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')