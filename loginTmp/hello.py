#import urllib2
import requests

CONSUMER_KEY = '77ivy1b3bzxmlk'     # This is api_key
CONSUMER_SECRET = 'yyZCB6IvxBFinBcO'   # This is secret_key

# https://www.linkedin.com/uas/oauth2/authorization
'''
https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=77ivy1b3bzxmlk&redirect_uri=https%3A%2F%2Fwww.google.com&state=987654321
'''
#r = requests.get('http://0.0.0.0:5000')
#1.pop some line
r = requests.post("http://0.0.0.0:5000")
print r