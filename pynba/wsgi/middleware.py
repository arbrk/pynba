"""
    Pynba
    ~~~~~

    :copyright: (c) 2015 by Xavier Barbosa.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import, unicode_literals

__all__ = ['PynbaMiddleware']

from .ctx import RequestContext
from pynba.core import Reporter


class PynbaMiddleware(object):
    """Used to decorate main apps.

    Properties:
        app (callable): The main WSGI app that will be monitored.
        address (str): The address to the UDP server.
        config (dict): basically optional parameters
    """

    default_ctx = RequestContext

    def __init__(self, app, address, **config):
        self.app = app
        self.reporter = Reporter(address)
        self.config = config

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            return self.app(environ, start_response)

    def request_context(self, environ):
        """
        :param environ: The WSGI environ mapping.
        :return: will return a new instance of :class:`~.ctx.RequestContext`
        """
        return self.default_ctx(self.reporter, environ, **self.config)