from django.shortcuts import render
from django.http import HttpResponse
import twilio.twiml

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

def hello(request):
	if request.method == 'POST':
		# the person who it was from, otherwise, None
		from_num = request.values.get('From', None)
		msg = "Your number is " + str(from_num)
		resp = twilio.twiml.Response()
		resp.message(msg)
		return HttpResponse(str(resp))
		
	elif request.method == 'GET':
	    resp = twilio.twiml.Response()
	    resp.message("get request")
	    return HttpResponse(str(resp))