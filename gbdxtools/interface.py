'''
Authors: Kostas Stamatiou, Dan Getman, Nate Ricklin, Dahl Winters, Donnie Marino
Contact: kostas.stamatiou@digitalglobe.com

Functions to interface with GBDX API.
'''

import json
import os
import logging

from gbdx_auth import gbdx_auth

from gbdxtools.s3 import S3
from gbdxtools.ordering import Ordering
from gbdxtools.workflow import Workflow
from gbdxtools.catalog import Catalog
from gbdxtools.idaho import Idaho


class Interface():

    gbdx_connection = None
    def __init__(self, **kwargs):
        if (kwargs.get('username') and kwargs.get('password') and 
            kwargs.get('client_id') and kwargs.get('client_secret')):
            self.gbdx_connection = gbdx_auth.session_from_kwargs(**kwargs)
        elif kwargs.get('gbdx_connection'):
            # Pass in a custom gbdx connection object, for testing purposes
            self.gbdx_connection = kwargs.get('gbdx_connection')
        else:
            # This will throw an exception if your .ini file is not set properly
            self.gbdx_connection = gbdx_auth.get_session()

        # create a logger
        # for now, just log to the console. We'll replace all the 'print' statements 
        # with at least logger.info or logger.debug statements
        # later, we can log to a service, file, or some other aggregator
        self.logger = logging.getLogger('gbdxtools')
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.info('Logger initialized')

        # create and store an instance of the GBDX s3 client
        self.s3 = S3(self)

        # create and store an instance of the GBDX Ordering Client
        self.ordering = Ordering(self)

        # create and store an instance of the GBDX Catalog Client
        self.catalog = Catalog(self)

        # create and store an instance of the GBDX Workflow Client
        self.workflow = Workflow(self)

        # create and store an instance of the Idaho Client
        self.idaho = Idaho(self)