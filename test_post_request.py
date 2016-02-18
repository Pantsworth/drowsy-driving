import requests
import urllib
import urllib2
import sys

# payload = {'threshold':'44'}
# url = "https://mhealth-demo.herokuapp.com/"

# r = requests.post("https://mhealth-demo.herokuapp.com/threshold",
# 	params=payload)

# print r.text
# print(r.status_code,r.reason)

# # print (r.text[:500] + '...')
# r = requests.get("http://mhealth-demo.herokuapp.com/readings/")
# print r.text

# print "-------------"

# data = urllib.urlencode(payload)
# req = urllib2.Request(url,data)
# response = urllib2.urlopen(req)
# the_page = response.read()
# print the_page

print "\n\n\n -------------------- \n\n "
yawn = 0
blink = 0
print sys.argv
if len(sys.argv)<2:
	yawn = 1
else:
	yawn = int(sys.argv[1])
if len(sys.argv)<3:
	blink = 11
else:
	blink = int(sys.argv[2])

payload = {'yawnRate':yawn , 'blinkRate':blink}
url = "https://mhealthhelloworld-bpeynetti.c9users.io/insert.php"
r = requests.post(url,data=payload)
print r.text