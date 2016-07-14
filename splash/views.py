from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
import urllib2, re, json, unicodedata

# makes the message the intro the corresponding wikipedia page
def wiki(search):
	try:
		response = urllib2.urlopen('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=' + search)
		data = json.loads(response.read())

		page = data['query']['pages'].keys()[0] # gets this pesky page ID

		intro = data['query']['pages'][page]['extract']

		if 'may refer to:' in intro:
			return 'Please be a little more specific!'
		else:
			intro = unicodedata.normalize('NFKD', intro).encode('ascii', 'ignore') # clean utf-8 chars
			
			pron = re.compile(r'\s\(\/.*\/\)') # clears out pronunciations
			intro = pron.sub('', intro)

			return intro


		# # gets wikpedia page
		# response = urllib2.urlopen('http://wikipedia.org/wiki/' + search)
		# html = response.read()

		# # just gets the introduction
		# intro = html[html.index('<p>') + 3:html.index('</p>')]

		# # regexes to clean up the text
		# tags = re.compile(r'<.*?>')
		# refs = re.compile(r'\[[0-9]\]')

		# intro = tags.sub('', intro)
		# intro = refs.sub('', intro)

		# return intro

	except:
		return 'Error! Your search term might not exist in the Wikipedia database :('

# Create your views here.
def index(request):
	return HttpResponse("placeholder ;)")

@twilio_view
def hello(request):
	# if POSTed to by twilio...
	if request.method == 'POST':
		# gets body of text, else None
		sub = request.POST.get('Body', None).split()
		query = sub[0] # first part is the query

		# twilio response
		r = Response() # makes messages object

		if query.lower() == 'wiki':
			term = '%20'.join(sub[1:]) # rest of their submission put together with %20s
			r.message(wiki(term))
		else:
			r.message('Invalid request')
		
		return HttpResponse(r.toxml(), content_type='text/xml')

	# if accessing the webpage via GET
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')
