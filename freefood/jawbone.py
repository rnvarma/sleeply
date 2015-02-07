import httplib, urllib2, json, time, datetime
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

def main(api_key):
	api_key = 'r5ZHAAV8pCX7UpqLgRy-i3Dzzi0ExmCCjrn_ztxZsWgYKibrZhpX6cYD-LXDCyL0_7thzXV5WO7OrZkZcuARr1ECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP'

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
	avgStart = avgStart/sleeps
	avgEnd = avgEnd/sleeps
	coffee = avgEnd-45
	coffeeNap = avgEnd-30
	sleep = avgStart-120
	if sleep < 0:
		sleep = 1440 - sleep
	clusters = clusters.tolist()

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

	date = datetime.datetime.now()
	shortnapdate = date;
	coffeedate = date;
	if shortNap > 240:
		shortnapdate += datetime.timedelta(days=1)
	if coffee > 240:
		shortnapdate += datetime.timedelta(days=1)
	increment = date + datetime.timedelta(days=1)
	return [{'title':'Short Nap', 
				'startTime' : (shortNap/60, shortNap%60),
				'endTime' : ((shortNap+20)/60,(shortNap+20)%60),
				'date' : shortnapdate},
			{'title':'Caffeine',
				'startTime' : (coffee/60, coffee%60),
				'endTime' : ((coffee+15)/60,(coffee+15)%60),
				'date' : coffeedate},
			{'title':'PowerNap',
				'startTime' : (coffeeNap/60, coffeeNap%60),
				'endTime' : ((coffeeNap+20)/60,(coffeeNap+20)%60),
				'date' : coffeedate},
			{'title':'Long Nap',
				'startTime' : (longNap/60, longNap%60),
				'endTime' : ((longNap+90)/60,(longNap+90)%60),
				'date' : increment},
			{'title':'ZzZzZzZz',
				'startTime' : (sleep/60, sleep%60),
				'endTime' : ((avgEnd)/60,(avgEnd)%60),
				'date' : increment}]

	
print main("")





