#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from . import log
from . import config


class Connector(object):
    session = requests.Session()

    def authenticate(self, domain, username, password):
        self.session.auth = (username, password)
        self.base = 'https://' + domain + '.leankit.com/kanban/api'

    def get(self, url):
        log.debug('GET {}'.format(url))
        try:
            request = self.session.get(self.base + url, verify=True)
        except Exception as error:
            raise IOError("Unable to make HTTP request: {}".format(error))
        if request.ok:
            try:
                response = request.json()
                if response['ReplyCode'] == 200:
                    return response['ReplyData'][0]
                else:
                    msg = "Error {ReplyCode}: {ReplyText}".format(**response)
                    raise ConnectionError(msg)

            except ValueError:
                raise IOError("Invalid response")
        else:
            msg = 'Server responded with code {0.status_code}'.format(request)
            raise ConnectionError(msg)


api = Connector()
api.authenticate(**config.credentials)
