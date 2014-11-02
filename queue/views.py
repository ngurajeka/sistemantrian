from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse
from .models import *
import datetime
import os

"define global variable"
context_dict = {
	'WebName': 'Kantor Pelayanan Pajak Pratama Bulukumba',
	'SmallWebName': 'KPP Pratama Bulukumba',
	'isLoket': False,
	'isHelpDesk': False,
	'myData': {},
	'myTipe': 0,
	'activeLink': 'Beranda',
	'WebMenu': Menu.objects.filter(permissions=0),
	'ShowMenu': True,
	'ToDayDate': datetime.datetime.now(),
}

"define some function to re-use"
def get_or_none(model, **kwargs):
	try:
		return model.objects.get(**kwargs)
	except model.DoesNotExist:
		return None

def setContextDict(request):
	global context_dict
	if request.user.is_authenticated():
		if request.user.is_staff:
			context_dict['myTipe'] = 4
			context_dict['WebMenu'] = Menu.objects.all()
		else:
			context_dict['myTipe'] = UserDetail.objects.get(user=request.user.id).category
			context_dict['myData'] = UserDetail.objects.get(user=request.user.id)
			context_dict['WebMenu'] = Menu.objects.filter(Q(permissions=context_dict['myTipe']) | Q(permissions=3) | Q(permissions=0))
	else:
		context_dict['myTipe'] = 0

def home(request):
	setContextDict(request)
	context = RequestContext(request)
	return render_to_response('site/home.html', context_dict, context)

def user_login(request):
	setContextDict(request)
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponse('Login successfull')
			else:
				return HttpResponse('Your account is not active')
		else:
			return HttpResponse("Login failed, please try again")
	else:
		return render_to_response('site/user/login.html', context_dict, context)

def panel_loket(request):
	setContextDict(request)
	context = RequestContext(request)
	context_dict['activeLink'] = 'Panel Loket'
	return render_to_response('site/panel/loket.html', context_dict, context)

def queue_add(request):
	setContextDict(request)
	context = RequestContext(request)
	context_dict['ShowMenu'] = False
	return render_to_response('site/queue/add.html', context_dict, context)

def queue_add_post(request):
	setContextDict(request)
	if request.is_ajax():
		if request.method == 'GET':
			thisDayStr = context_dict['ToDayDate'].strftime("%A")
			thisDay = 0
			if thisDayStr == 'Monday':
				thisDay = 1
			elif thisDayStr == 'Tuesday':
				thisDay = 2
			elif thisDayStr == 'Wednesday':
				thisDay = 3
			elif thisDayStr == 'Thursday':
				thisDay = 4
			elif thisDayStr == 'Friday':
				thisDay = 5
			elif thisDayStr == 'Saturday':
				thisDay = 6
			elif thisDayStr == 'Sunday':
				thisDay = 7
			thisCat = request.GET.get('queueCatRadios', None)
			thisOrderNumber = request.GET.get('queueOrderNumber', None)
			thisProcess = 0
			thisDate = datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day)
			if thisDay is not 0 and thisCat is not None and thisOrderNumber is not None:
				thisData = QueueList(day=thisDay,category_id=int(thisCat),order_number=thisOrderNumber,process=thisProcess,date=thisDate)
				try:
					thisData.save()
					return HttpResponse("successfull")
				except IntegrityError:
					return HttpResponse("error IntegrityError")
			else:
				return HttpResponse("error data")
		else:
			return HttpResponse("error method")
	else:
		return HttpResponse("access restricted")

def getQueueOrderNumber(request):
	setContextDict(request)
	if request.is_ajax():
		thisCat = int(request.GET.get('category', None))
		thisData = QueueList.objects.filter(category_id=thisCat,date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day))
		return HttpResponse(thisData.count()+1)
	else:
		return HttpResponse("access restricted")

def getRemainingQueue(request):
	setContextDict(request)
	if request.is_ajax():
		remaining = QueueList.objects.filter(process=0,date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day),category=int(request.GET.get('category', None)))
		return HttpResponse(remaining.count())
	else:
		return HttpResponse("access restricted")

def getOnGoingQueue(request):
	setContextDict(request)
	if request.is_ajax():
		ongoing = QueueOnGoing.objects.filter(user=request.GET.get('user', None))
		if ongoing.count() is not 0:
			return HttpResponse(ongoing[0].queue.order_number)
		else:
			return HttpResponse(0)
	else:
		return HttpResponse("access restricted")

def getQueueForPanelLoket(request):
	setContextDict(request)
	thisCat = int(request.GET.get('category', None))
	thisUser = int(request.GET.get('loket', None))
	remaining = QueueList.objects.filter(process=0,date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day),category=thisCat).count()
	ongoing = QueueOnGoing.objects.filter(date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day),user_id=thisUser)
	if ongoing.count() is not 0:
		ongoingorder = QueueList.objects.get(pk=ongoing.first().queue_id).order_number
	else:
		ongoingorder = 0
	data = '[{"category": '+str(thisCat)+', "loket": '+str(thisUser)+', "ongoing": '+str(ongoingorder)+', "remaining": '+str(remaining)+'}]'
	return HttpResponse(data, content_type='application/json')

def queueCallNext(request):
	setContextDict(request)
	thisCat = int(request.POST['category'])
	thisUser = int(request.POST['user'])
	data = QueueList.objects.filter(process=0,date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day),category=thisCat)
	ongoing = QueueOnGoing.objects.filter(date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day),user_id=thisUser)
	if ongoing.count() is not 0:
		newOngoing = QueueOnGoing.objects.get(pk=ongoing.first().pk)
		newOngoing.queue_id = data.first().pk
		newOngoing.save()
	else:
		newOngoing = QueueOnGoing(queue_id=data.first().pk,user_id=thisUser,date=datetime.date(context_dict['ToDayDate'].year, context_dict['ToDayDate'].month, context_dict['ToDayDate'].day))
		newOngoing.save()
	newData = QueueList.objects.get(pk=data.first().pk)
	newData.process=1
	newData.save()
	os.system("amixer")
	return HttpResponse("successfull")