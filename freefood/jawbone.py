import httplib, urllib2, json, time, datetime, random
from scipy.cluster.vq import kmeans, whiten
import numpy as np

def innerMap(shit):
	if int(shit['depth']) == 3:
		timeStart = time.gmtime(int(shit['time']))
		start = timeStart.tm_hour*60 + timeStart.tm_min
		return [start]
	return []

def mapWrapped(api_key):
	def mapShit(shit):
		details = shit['details']
		xid = shit['xid']
		key = 'Bearer ' + api_key
		request = urllib2.Request('https://jawbone.com/nudge/api/v.1.1/sleeps/' + xid + '/ticks')
		request.add_header("Authorization", "Bearer %s" % api_key)
		result = urllib2.urlopen(request)
		phases = json.loads(result.read())['data']['items']

		stuff = []
		mapped = map (innerMap, phases)
		for item in mapped:
			if len(item) > 0:
				stuff.append(item[0])

		if int(shit['sub_type']) == 0:
			timeStart = time.gmtime(int(details['asleep_time']))
			timeEnd = time.gmtime(int(details['awake_time']))
			start = timeStart.tm_hour*60 + timeStart.tm_min
			end = timeEnd.tm_hour*60 + timeEnd.tm_min
			return (start, end, 1,stuff)
		return (0,0,0,stuff)
	return mapShit

def reduceShit((a,b,c,g), (d,e,f,h)):
	return (a+d,b+e,c+f,[])

def conflicts(calendar, (start, end)):
	for (event_start, event_end) in calendar:
		if end >= event_start and start <= event_end:
			return (event_start, event_end)

def simpleMapWrapped(api_key):
	def simpleMap(shit):
		details = shit['details']
		if int(shit['sub_type']) == 0:
			timeStart = time.gmtime(int(details['asleep_time']))
			timeEnd = time.gmtime(int(details['awake_time']))
			start = timeStart.tm_hour*60 + timeStart.tm_min
			end = timeEnd.tm_hour*60 + timeEnd.tm_min
			return (start, end, 1)
		return (0,0,0)
	return simpleMap

def simpleReduce((a,b,c),(d,e,f)):
	return (a+d,b+e,c+f)

def avgsleepwake(api_key):
	request = urllib2.Request("https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?limit=1000")
	request.add_header("Authorization", "Bearer %s" % api_key)
	result = urllib2.urlopen(request)
	dataShits =  json.loads(result.read())['data']['items']
	(avgStart, avgEnd, sleeps) = reduce (simpleReduce, map (simpleMapWrapped(api_key),dataShits), (0,0,0))
	startTime = datetime.time((avgStart/sleeps)/60, (avgStart/sleeps)%60)
	endTime = datetime.time((avgEnd/sleeps)/60, (avgEnd/sleeps)%60)
	return (startTime, endTime)

def calculate(api_key):
	request = urllib2.Request("https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?limit=100")
	request.add_header("Authorization", "Bearer %s" % api_key)
	result = urllib2.urlopen(request)
	dataShits =  json.loads(result.read())['data']['items']
	fourThings = map (mapWrapped(api_key),dataShits)
	(avgStart, avgEnd, sleeps, _) = reduce(reduceShit,fourThings, (0,0,0,[]))
	phases = []
	for _,_,_,thing in fourThings:
		phases.extend(thing)
	mapped = map(lambda f: np.array([float(f)]), phases)
	array = kmeans(np.array(mapped), 3)
	clusters = array[0]
	clusters = clusters.tolist()
	avgStart = avgStart/sleeps
	avgEnd = avgEnd/sleeps
	return (avgStart, avgEnd, sleeps, clusters)

def allnighter(api_key, calendar, date):
	#REMOVE THIS DUMMY VALUE BEFORE USING!!!!!!
	api_key = 'r5ZHAAV8pCX7UpqLgRy-i3Dzzi0ExmCCjrn_ztxZsWgYKibrZhpX6cYD-LXDCyL0_7thzXV5WO7OrZkZcuARr1ECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP'

	(avgStart, avgEnd, sleeps, clusters) = calculate(api_key)
	coffee = avgEnd-45
	coffeeNap = avgEnd-30
	sleep = avgStart-120
	if sleep < 0:
		sleep = 1440 - sleep

	if avgEnd > avgStart:
		end = avgEnd - avgStart
	else:
		end = (1440 - avg_start) + avgEnd
	shortNap = -1
	longNap = -1
	for cluster in clusters:
		scaled = 0
		if cluster[0] > avgStart:
			scaled = int(cluster[0]) - avgStart
		else:
			scaled = (1440 - avg_start) + int(cluster[0])
		if 0 < scaled and scaled < (end - 100) :
			shortNap = int(cluster[0])
		elif end < scaled :
			longNap = int(cluster[0])

	shortnapdate = date
	coffeedate = date
	coffeenapdate = date
	if shortNap < 1260:
		shortnapdate += datetime.timedelta(days=1)
		shortnapdate = datetime.datetime.combine(shortnapdate, datetime.time(shortNap/60, shortNap%60))
	if coffee < 1260:
		coffeedate += datetime.timedelta(days=1)
		coffeenapdate = datetime.datetime.combine(coffeedate, datetime.time(coffeeNap/60, coffeeNap%60))
		coffeedate = datetime.datetime.combine(coffeedate, datetime.time(coffee/60, coffee%60))
	increment = date + datetime.timedelta(days=1)
	if sleep < 960:
		increment = increment + datetime.timedelta(days=2)
	longnapdate = datetime.datetime.combine(increment, datetime.time(longNap/60, longNap%60))
	sleepdate = datetime.datetime.combine(increment, datetime.time(sleep/60, sleep%60))
	dictArray = []
	events = [	("Excercise", shortnapdate, 20),
				("Caffeine", coffeedate, 15),
				("PowerNap", coffeenapdate, 20),
				("Long Nap", longnapdate, 90),
				("ZzZzZzZz", sleepdate, 600)]
	for event in events:
		endtime = event[1] + datetime.timedelta(minutes=event[2])
		c = conflicts(calendar, (event[1], endtime))
		if c == None or event[0] == 'ZzZzZzZz':
			dictArray.append({'title':event[0], 
							'startTime' : event[1],
							'endTime' : endtime})
		else:
			endtime = c[0]
			starttime = endtime - datetime.timededlta(minutes=event[2])
			d = conflicts(calendar, (starttime, endtime))
			if d == None:
				dictArray.append({'title':event[0],
								'startTime':starttime,
								'endTime': endtime})
			else:
				starttime=c[1]
				endtime = starttime + datetime.timededlta(minutes=event[2])
				d = conflicts(calendar, (starttime, endtime))
				if d == None:
					dictArray.append({'title':event[0],
								'startTime':starttime,
								'endTime': endtime})
	return dictArray

def regular(api_key, calendar):
	#calendar is a 2d array of the form [[Monday],[Tuesday],[Wednesday]...]
	# this is because that makes things easier for me. thanks. 
	api_key = 'r5ZHAAV8pCX7UpqLgRy-i3Dzzi0ExmCCjrn_ztxZsWgYKibrZhpX6cYD-LXDCyL0_7thzXV5WO7OrZkZcuARr1ECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP'
	(avgStart, avgEnd, sleeps, clusters) = calculate(api_key)
	if avgEnd > avgStart:
		length = avgEnd - avgStart
	else:
		length = (1440 - avg_start) + avgEnd
	request = urllib2.Request("https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps")
	request.add_header("Authorization", "Bearer %s" % api_key)
	request.add_header("start_time", str(time.time() - 604800))
	request.add_header("end_time", str(time.time()))
	result = urllib2.urlopen(request)
	dataShits =  json.loads(result.read())['data']['items']
	duration = 0
	for shit in dataShits:
		duration += (shit['details']['duration'])
	duration = (duration/60)/7
	makeup = 0
	if duration < max(length, 480):
		makeup = max(2*(length-duration), 30)
	if makeup == 0:
		return None
	if avgEnd > avgStart:
		end = avgEnd - avgStart
	else:
		end = (1440 - avg_start) + avgEnd
	for cluster in clusters:
		scaled = 0
		if cluster[0] > avgStart:
			scaled = int(cluster[0]) - avgStart
		else:
			scaled = (1440 - avg_start) + int(cluster[0])
		if 0 < scaled and scaled < (end - 100) :
			shortNap = int(cluster[0])
		elif end < scaled :
			longNap = int(cluster[0])
	napNames = ['nap','snooze','doze','shut-eye','sshhhhhh']
	dictArray = []
	times = [20,30,40,50]
	date = datetime.date.today()
	date = datetime.datetime.combine(date, datetime.time(longNap/60, longNap%60))
	for i in range (0,7):
		coin = random.randint(0,4)
		if coin < 2:
			current = date + datetime.timedelta(days=i)
			endtime = date + datetime.timedelta(minutes=makeup)
			c = conflicts(calendar[i], (current, endtime))
			if c == None:
				dictArray.append({'title':napNames[random.randint(0,4)], 
								'startTime' : current,
								'endTime' : endtime})
			else:
				endtime = c[0]
				starttime = endtime - datetime.timededlta(minutes=makeup)
				d = conflicts(calendar, (starttime, endtime))
				if d == None:
					dictArray.append({'title':napNames[random.randint(0,4)],
									'startTime':starttime,
									'endTime': endtime})
				else:
					starttime=c[1]
					endtime = starttime + datetime.timededlta(minutes=makeup)
					d = conflicts(calendar, (starttime, endtime))
					if d == None:
						dictArray.append({'title':napNames[random.randint(0,4)],
									'startTime':starttime,
									'endTime': endtime})
		# coin = random.randint(0,2)
		# if coin == 1 and not len(calendar) == 0:
		# 	leng = len(calendar[i]) - 1
		# 	c = calendar[i][random.randint(0,leng)]
		# 	endtime = c[0]
		# 	starttime = endtime - datetime.timedelta(minutes=times[random.randint(0,3)])
		# 	d = conflicts(calendar, (starttime, endtime))
		# 	if d == None:
		# 		dictArray.append({'title':'Be Productive!',
		# 						'startTime':starttime,
		# 						'endTime': endtime})
		# 	else:
		# 		starttime=c[1]
		# 		endtime = starttime + datetime.timededlta(minutes=random.randint(2)*times[random.randint(0,3)])
		# 		d = conflicts(calendar, (starttime, endtime))
		# 		if d == None:
		# 			dictArray.append({'title':'Be Productive',
		# 						'startTime':starttime,
		# 						'endTime': endtime})
		# if coin == 0 and not len(calendar) == 0:
		# 	leng = len(calendar[i]) - 1
		# 	c = calendar[i][random.randint(0,leng)]
		# 	endtime = c[0]
		# 	starttime = endtime - datetime.timedelta(minutes=times[random.randint(0,3)])
		# 	d = conflicts(calendar, (starttime, endtime))
		# 	if d == None:
		# 		dictArray.append({'title':'Relax!',
		# 						'startTime':starttime,
		# 						'endTime': endtime})
		# 	else:
		# 		starttime=c[1]
		# 		endtime = starttime + datetime.timededlta(minutes=random.randint(2)*times[random.randint(0,3)])
		# 		d = conflicts(calendar, (starttime, endtime))
		# 		if d == None:
		# 			dictArray.append({'title':'Relax',
		# 						'startTime':starttime,
		# 						'endTime': endtime})
	return dictArray








# print regular("",[[],[(datetime.datetime.now()+datetime.timedelta(days=2), datetime.datetime.now() + datetime.timedelta(minutes=53) + datetime.timedelta(days=2))],[],[],[],[],[]])
# print allnighter("", [(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=5))])
# print avgsleepwake('r5ZHAAV8pCX7UpqLgRy-i3Dzzi0ExmCCjrn_ztxZsWgYKibrZhpX6cYD-LXDCyL0_7thzXV5WO7OrZkZcuARr1ECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP')





