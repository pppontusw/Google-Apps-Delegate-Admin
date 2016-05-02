# Google-Apps-Delegate-Admin

## What is it?

This is a tool to manage Mail delegations on Google Apps.

## What do you have to do?

1. Generate and put your own client_secrets.json in this folder
2. Install dependencies

You can also install it using my [ansible role](https://github.com/pppontusw/ansible-Google-Apps-Delegate-Admin)

```
pip install flask flask-wtf xmltodict httplib2 oauth2client
```
3. ```python -m run``` and go to localhost:5000

!["Screenshot"](http://i.imgur.com/9QlLvn0.png)

## Generating client_secrets.json

[See here for instructions](https://developers.google.com/api-client-library/python/guide/aaa_oauth#acquiring--client-ids-and-secrets)
