import datetime
import requests
import json
import platform
import subprocess
import concurrent.futures
import time

# dl = [651, 650, 141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142, ]
# thresh = 0
# min_age_limit = 18


headers = {
	"authority" : """cdn-api.co-vin.in""",
	"accept" : """application/json, text/plain, */*""",
	"dnt" : """1""",
	"sec-ch-ua-mobile" : """?0""",
	"user-agent" : """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36""",
	"origin" : """https://www.cowin.gov.in""",
	"sec-fetch-site" : """cross-site""",
	"sec-fetch-mode" : """cors""",
	"sec-fetch-dest" : """empty""",
	"referer" : """https://www.cowin.gov.in/""",
	"accept-language" : """en-US,en;q=0.9"""
}


def filter_sessions_on_age_thresh(centre_list):
	for centre in centre_list:
		centre['sessions'] = filter(lambda session: session['min_age_limit'] == min_age_limit and session['available_capacity'] >= thresh, centre['sessions'])


def notify(notification_list):
	if platform.system() == 'Darwin':
		command_func = lambda n: (["osascript", "-", "e"], 'display notification "{}" with title "Vaccination Centre found" sound name "default"'.format(n))
	else:
		raise "Platform not supported"

	for n in notification_list:
		cmd, cmd_input = command_func(n)
		sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
		print(sp.communicate(cmd_input))


def get_notifications(date, dist_list):
	notification_list = []
	for dist in dist_list:
		for centre in dist['centers']:
			if list(centre['sessions']):
				notification_list.append('You have Vaccines available in District : {} \n Centre : {} on {}'.format(centre['district_name'], centre['address'], date.strftime('%d-%m-%Y')))
				print("District Found : {}".format(dist))
				print("Session : {}".format(list(centre['sessions'])))
	return notification_list


def poll(date):
	# poll and notify based on the parameters
	print("Checking for date : {}".format(date.strftime('%d-%m-%Y')))
	def dist_poller(dist_id):
		url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_id, date.strftime('%d-%m-%Y'))
		cowin_resp = requests.get(url, headers=headers)
		parsed_cowin_resp = json.loads(cowin_resp.content)
		centers = parsed_cowin_resp['centers']
		filter_sessions_on_age_thresh(centers)
		return parsed_cowin_resp

	dist_resp_list = []

	with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
		poller_futures = [executor.submit(dist_poller, dist_id) for dist_id in dl]
		for poller_future in concurrent.futures.as_completed(poller_futures):
			dist_resp_list.append(poller_future.result())

	notifications = get_notifications(date, dist_resp_list)
	notify(notifications)


def dates_poller():
	today = datetime.date.today()
	polling_date_list = [
		today,
	]
	list(map(lambda w: polling_date_list.append(today + datetime.timedelta(days=-today.weekday(), weeks=w)), 
			 [1,2,3]))


	with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
		executor.map(poll, polling_date_list)

	# for d in polling_date_list:
	# 	print("Checking for date : {}".format(d.strftime('%d-%m-%Y')))
	# 	poll(d)

if __name__ == "__main__":
	global thresh
	global dl
	global min_age_limit
	global polling_interval

	# dl = [651, 650, 141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142, ]
	# thresh = 0
	# min_age_limit = 18

	dl = [int(did.strip()) for did in input("Enter list of districts ids (comma separated) : ").split(',')]
	thresh = int(input("Enter minimum number of slots (per centre in district) available to notify : "))
	min_age_limit = int(input("Enter minimum age (18/45) : "))
	polling_interval = int(input("Enter Polling interval in seconds : "))

	while True:
		dates_poller()
		time.sleep(polling_interval)


