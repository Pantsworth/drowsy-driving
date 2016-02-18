import requests
import urllib
import urllib2

payload = {'threshold':'44'}
url = "https://mhealth-demo.herokuapp.com/"

r = requests.post("https://mhealth-demo.herokuapp.com/threshold",
	params=payload)

print r.text
print(r.status_code,r.reason)

# print (r.text[:500] + '...')
r = requests.get("http://mhealth-demo.herokuapp.com/readings/")
print r.text

print "-------------"

# data = urllib.urlencode(payload)
# req = urllib2.Request(url,data)
# response = urllib2.urlopen(req)
# the_page = response.read()
# print the_page

print "\n\n\n -------------------- \n\n "
payload = {'angle':33 , 'word':'hello'}
url = "https://mhealthhelloworld-bpeynetti.c9users.io/insert.php"
r = requests.post(url,data=payload)
print r.text