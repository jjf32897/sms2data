from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml import Response

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

@csrf_exempt
def hello(request):
	if request.method == 'POST':
		r = Response()
		r.message('i said HEY WHAT\'S UP HELLO')
		return HttpResponse(r.toxml(), content_type='text/xml')
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')