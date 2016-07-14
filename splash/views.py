from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
import urllib2, re

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

@twilio_view
def hello(request):
	# if POSTed to by twilio...
	if request.method == 'POST':
		# gets body of text, else None
		search = request.POST.get('Body', None)

		# twilio response
		r = Response() # makes messages object

		try:
			# gets wikpedia page
			response = urllib2.urlopen('http://wikipedia.org/wiki/' + search)
			html = response.read()

			# just gets the introduction
			intro = html[html.index('<p>') + 3:html.index('</p>')]

			# regexes to clean up the text
			tags = re.compile(r'<.*?>')
			refs = re.compile(r'\[[0-9]\]')

			intro = tags.sub('', intro)
			intro = refs.sub('', intro)

			r.message(intro)

		except:
			r.message('Error, try again soon')

		return HttpResponse(r.toxml(), content_type='text/xml')

	# if accessing the webpage via GET
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')