from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
from .models import Dataset, Element
import urllib2, re, json, unicodedata, zlib

# makes the message the intro the corresponding wikipedia page (riddled with bugs/edge cases)
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

	except:
		return 'Error! Your search term might not exist in the Wikipedia database :('

# sends the title and top answer of the top result for the stack overflow question related to the search terms
def stack(search):
	# collects json. it looks like it's gzipped, so we'll deal with that
	response = urllib2.urlopen('https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' + search + '&site=stackoverflow')
	decompressed = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
	data = json.loads(decompressed) # turn string into JSON dict
	if data['items']: # if there are questions resulting from the query, get the top answer of the first one
		top = data['items'][0]
		if top['is_answered']: # if it has an accepted answer
			pass

	else:
		return 'Error! Couldn\'t find a relevant StackOverflow question :('

# good ol' index page
def index(request):
	return render(request, 'index.html')

def store(request):
	# if they're POSTing
	if request.method == 'POST':
		num = request.POST.get('phone').replace('(', '').replace(')', '').replace('-', '') # filter out parens and hyphens
		code = request.POST.get('code')
		data = request.POST.get('data')
		dtype = request.POST.get('dtype')

		if len(num) > 0 and len(code) > 0 and len(data) > 0:
			if len(num) != 10 or not num.isdigit(): # if it's not a valid phone number
				return render(request, 'index.html', {'notif': 'invalid phone number'})
			else:
				# make the element
				# if it's media
				if dtype == "mms":
					element = Element(datum=data)
				else: # otherwise
					element = Element(datum=data, is_media=False)

				element.save()

				# make the dataset and give it the element
				dataset = Dataset(number='+1' + num, identifier=code)
				dataset.save()

				dataset.elements.add(element)

				return render(request, 'index.html', {'notif': 'your submission was successful'})
		
		else:
			return render(request, 'index.html', {'notf': 'fill out form completely'})

	# if they're GETting
	else:
		return HttpResponseRedirect('/')

@twilio_view
def hello(request):
	# if POSTed to by twilio...
	if request.method == 'POST':
		# gets body of text, else None
		identifier = request.POST.get('Body', None)
		# query = sub[0].lower() # first part is the query, lowercased to avoid those annoying issues
		number = request.POST.get('From', None) # gets the user's number

		dataset = Dataset.objects.get(number=number, identifier=identifier.lower()) # retrieves the corresponding dataset

		# twilio response
		r = Response() # makes messages object

		with r.message('Requested images:') as m:
			if dataset is not None:
				for element in dataset.elements.all():
					if element.is_media: # if it's a media URL, add it as a media tag to the response XML
						m.media(element.datum)
		
		# if query == 'hold': # hold on to a piece of data

		# elif query == 'give': # retrieve a piece of data

		# elif query == 'code':
		# 	pass
		# elif query == 'wiki': # wiki the term and return the intro
		# 	term = '%20'.join(sub[1:]) # rest of their submission put together with %20s
		# 	r.message(wiki(term))
		# else:
		# 	r.message('Invalid request')
		
		return HttpResponse(r.toxml(), content_type='text/xml')

	# if accessing the webpage via GET
	elif request.method == 'GET':
		return HttpResponse('bro why don\'t you just GET out of here.')
