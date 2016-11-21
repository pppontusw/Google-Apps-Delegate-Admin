#!/usr/bin/env python
# -*- coding: utf-8 -*-
from run import app
import pytest, uuid

app.config['WTF_CSRF_ENABLED'] = False
app.secret_key = str(uuid.uuid4())

def test_home_page_redirect():
    app.config['TESTING'] = False
    test_client = app.test_client()
    rsp = test_client.get('/')
    assert rsp.status == '302 FOUND'

def test_oauth_redirect():
    app.config['TESTING'] = False
    test_client = app.test_client()
    rsp = test_client.get('/')
    html = rsp.get_data(as_text=True)
    assert '<a href="/oauth2callback">/oauth2callback</a>' in html

def test_home_page():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<h3>Search for an account to manage delegates for</h3>' in html

def test_search():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.post('/search', data={'finddelegate': 'test.user@example.com'})
    assert rsp.status == '302 FOUND'
    html = rsp.get_data(as_text=True)
    assert '<a href="/delegate/example.com/test.user">' in html
    rsp = test_client.post('/search', data={'finddelegate': 'test.use'})
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'Not a valid email address!' in html

def test_add_delegate():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.post('/delegateto/example.com/danger', data={'newdelegate': 'test.use'})
    assert rsp.status == '302 FOUND'
    html = rsp.get_data(as_text=True)
    assert '<a href="/errgetdelegate/example.com/danger/Not%20a%20valid%20email%20address">/errgetdelegate/example.com/danger/Not%20a%20valid%20email%20address</a>' in html
    rsp = test_client.post('/delegateto/example.com/danger', data={'newdelegate': 'test.user@example.com'})
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'https://apps-apis.google.com/a/feeds/emailsettings' in html

def test_delete_delegate():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.get('/delegateto/example.com/test.user/danger')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/example.com/test.user/delegation/danger' in html

def test_err_get_delegate():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.get('/errgetdelegate/example.com/test.user/testerror')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/example.com/test.user/delegation' in html

def test_get_delegate():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.get('/delegate/example.com/test.user')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/example.com/test.user/delegation' in html

def test_error():
    app.config['TESTING'] = True
    test_client = app.test_client()
    rsp = test_client.get('/error/TEST')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<div class="alert alert-danger" role="alert"><span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span> TEST' in html