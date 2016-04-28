import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client

from xml.etree import ElementTree as ET

import gdata.apps.emailsettings.client

import xmltodict

app = flask.Flask(__name__)

@app.route('/delegate/<domain>/<username>')
def getdelegate(domain, username):
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		http_auth = credentials.authorize(httplib2.Http())
		url_get = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/' + domain + '/' + username + '/delegation'
		r = http_auth.request(url_get, "GET")
		jsondict = xmltodict.parse(r[1])
		jsondict = jsondict['feed']
		if (jsondict.has_key('entry')):
			jsondict = jsondict['entry']
		else:		
			return "Account not delegated."
		delegatearray = []
		if (isinstance(jsondict, dict)):
			jsondict = jsondict['apps:property'][0]
			return "Account delegated to: " + (jsondict['@value'])
		else:
			for entry in jsondict:
				entry = entry['apps:property'][1]['@value']
				delegatearray.append("Account delegated to: " + entry)
			return json.dumps(delegatearray)


@app.route('/')
def index():
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		http_auth = credentials.authorize(httplib2.Http())
		#url_get = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/domain/username/label'
		#r = http_auth.request(url_get, "GET")

		#xm = xmltodict.parse(r[1])
		#a = xm['feed']
		#a = a['entry']
		#a = a[0]
		#a = a['apps:property']
		#a = a[1]
		#a = a['@value']

		return "Welcome"


@app.route('/oauth2callback')
def oauth2callback():
 	flow = client.flow_from_clientsecrets(
		'client_secrets.json',
		scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
		redirect_uri=flask.url_for('oauth2callback', _external=True))
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		print(auth_uri)
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = True
	app.run()