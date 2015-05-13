import flask
import json
import requests
application = flask.Flask(__name__)


d = 'hello_world'
@application.route('/',methods=['GET', 'POST'])
def hello_world():
	d = str(flask.request.data)
	return d

@application.route('/data')
def data():
	d = flask.request.args
	payload = {'grant_type': 'authorization_code', 'code': 'code','redirect_uri':'http://helloen.elasticbeanstalk.com/data','client_id':'77ivy1b3bzxmlk'}
	r = requests.post("http://0.0.0.0:5000",data=json.dumps(payload))
	return str(d)


if __name__ == '__main__':
    application.run()