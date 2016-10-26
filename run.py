import json
import flask
from flask import render_template
import httplib2
from oauth2client import client
import xmltodict
from forms import DelegateForm, SearchForm
import re
import uuid

app = flask.Flask(__name__)

@app.route('/delegateto/<domain>/<username>', methods=['POST'])
def adddelegate(domain, username):
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		http_auth = credentials.authorize(httplib2.Http())
		form = DelegateForm()
		if form.validate_on_submit():
			newdelegate = form.data['newdelegate']
			if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", newdelegate):
				newform = SearchForm()
				searchform = SearchForm()
				err= 'Not a valid email address'
				return flask.redirect(flask.url_for('errgetdelegate', username=username, domain=domain, err=err))
			domainfilter = "^[A-Za-z0-9\.\+_-]+@" + domain + "$"
			if not re.match(domainfilter, newdelegate):
				newform = SearchForm()
				searchform = SearchForm()
				err = 'Delegate must be in the same email domain'
				return flask.redirect(flask.url_for('errgetdelegate', username=username, domain=domain, err=err))
			url_get = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/' + domain + '/' + username + '/delegation'
			xml = '<?xml version="1.0" encoding="utf-8"?><atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006"><apps:property name="address" value="%(newdelegate)s" /></atom:entry>'
			data = {'newdelegate': newdelegate}
			a = xml%data
			r = http_auth.request(url_get, method="POST", body=a, headers={'content-type': 'application/atom+xml; charset=UTF-8; type=entry'})
			return flask.redirect(flask.url_for('getdelegate', username=username, domain=domain))
		

@app.route('/delegateto/<domain>/<username>/<email>', methods=['GET'])
def deletedelegate(domain, username, email):
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		http_auth = credentials.authorize(httplib2.Http())
		url_get = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/' + domain + '/' + username + '/delegation/' + email
		r = http_auth.request(url_get, method="DELETE")
		return flask.redirect(flask.url_for('getdelegate', username=username, domain=domain))


@app.route('/delegate/<domain>/<username>', methods=['GET'])
def getdelegate(domain, username):
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		http_auth = credentials.authorize(httplib2.Http())
		url_get = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/' + domain + '/' + username + '/delegation'
		content = http_auth.request(url_get, "GET", headers={'cache-control': 'no-cache'})
		jsondict = xmltodict.parse(content[1])
		if (jsondict.has_key('HTML')):
			err = 'Not a valid domain or insufficient access!'
			return flask.redirect(flask.url_for('errorIndex', err=err))
		else:
			try:
				jsondict = jsondict['feed']
			except KeyError:
				err = 'This account does not seem to exist or another issue has resulted in an invalid response from Google'
				return flask.redirect(flask.url_for('errorIndex', err=err))
			form = DelegateForm()
			searchform = SearchForm()
			postlink = '/delegateto/' + domain + '/' + username
			if (jsondict.has_key('entry')):
				jsondict = jsondict['entry']
			else:		
				return render_template('delegate.html',
										postlink=postlink,
										form=form,
										searchform=searchform)
			delegatearray = []
			if (isinstance(jsondict, dict)):
				jsondict = jsondict['apps:property'][1]['@value']
				return render_template('delegate.html',
										delegate=jsondict,
										postlink=postlink,
										form=form,
										searchform=searchform)
			else:
				for entry in jsondict:
					entry = entry['apps:property'][1]['@value']
					delegatearray.append(entry)
				return render_template('delegate.html',
										delegates=delegatearray,
										postlink=postlink,
										form=form,
										searchform=searchform)


@app.route('/errgetdelegate/<domain>/<username>/<err>', methods=['GET'])
def errgetdelegate(domain, username, err):
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
		if (jsondict.has_key('HTML')):
			err = 'Not a valid domain or insufficient access!'
			return flask.redirect(flask.url_for('errorIndex', err=err))
		else:
			jsondict = jsondict['feed']
			form = DelegateForm()
			searchform = SearchForm()
			postlink = '/delegateto/' + domain + '/' + username
			if (jsondict.has_key('entry')):
				jsondict = jsondict['entry']
			else:		
				return render_template('delegate.html',
										postlink=postlink,
										form=form,
										searchform=searchform,
										error=err)
			delegatearray = []
			if (isinstance(jsondict, dict)):
				jsondict = jsondict['apps:property'][1]['@value']
				return render_template('delegate.html',
										delegate=jsondict,
										postlink=postlink,
										form=form,
										searchform=searchform,
										error=err)
			else:
				for entry in jsondict:
					entry = entry['apps:property'][1]['@value']
					delegatearray.append(entry)
				return render_template('delegate.html',
										delegates=delegatearray,
										postlink=postlink,
										form=form,
										searchform=searchform,
										error=err)


@app.route('/')
def index():
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		form = SearchForm()
		searchform = SearchForm()
		return render_template('index.html',
								form=form,
								searchform=searchform)


@app.route('/error/<err>')
def errorIndex(err):
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		form = SearchForm()
		searchform = SearchForm()
		return render_template('index.html',
								form=form,
								searchform=searchform,
								error=err)


@app.route('/search', methods=['POST'])
def search():
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		form = SearchForm()
		if form.validate_on_submit():
			email = form.data['finddelegate']
			if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
				newform = SearchForm()
				searchform = SearchForm()
				return render_template('index.html',
										form=newform,
										searchform=searchform,
										error='Not a valid email address!')
			else:
				a = email.split('@')
				url = 'delegate/' + a[1] + '/' + a[0]
				return flask.redirect(flask.url_for('getdelegate', username=a[0], domain=a[1]))
		else:
			return render_template('index.html',
									form=form,
									searchform=form,
									error='Is the field empty?')


@app.route('/search', methods=['GET'])
def getsearch():
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		return flask.redirect(flask.url_for('index'))


@app.route('/oauth2callback')
def oauth2callback():
 	flow = client.flow_from_clientsecrets(
		'client_secrets.json',
		scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
		redirect_uri=flask.url_for('oauth2callback', _external=True))
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
	app.config['WTF_CSRF_ENABLED'] = True
	app.secret_key = str(uuid.uuid4())
	app.debug = False
	app.run(host='0.0.0.0')