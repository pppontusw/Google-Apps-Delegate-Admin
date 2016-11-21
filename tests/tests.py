#!/usr/bin/env python
# -*- coding: utf-8 -*-
from run import app

def test_home_page():
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '302 FOUND'

def test_oauth_redirect():
    client = app.test_client()
    rsp = client.get('/')
    html = rsp.get_data(as_text=True)
    assert '<a href="/oauth2callback">/oauth2callback</a>' in html

def test_private_page():
    client = app.test_client()
    rsp = client.get('/report/private/test')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<input class="form-control" id="name" name="name" placeholder="Your name" type="text" value="">' in html
    assert '<input class="form-control" id="reason" name="reason" placeholder="Specify a reason for unblocking this site" type="text" value="">' in html

def test_guest_page():
    client = app.test_client()
    rsp = client.get('/report/guest/test')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<input class="form-control" id="name" name="name" placeholder="Your name" type="text" value="">' in html
    assert '<input class="form-control" id="reason" name="reason" placeholder="Specify a reason for unblocking this site" type="text" value="">' in html

def test_make_request():
    resp = views.makeRequest("TEST", "private", "Python Test Runner", "Tests must be done.")
    assert resp == 'Request was sent successfully and will be investigated. If you want more information, please follow up by emailing %s' % ADMIN_EMAIL
