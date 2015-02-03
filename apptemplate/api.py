# -*- coding: utf-8 -*-

'''
AppTemplate
===========
Python AppTemplate.
'''


class App(object):

    defaults = {
        'debug': False,
        'key_a': ['a1', 'a2', 'a3'],
        'key_b': 'VarB'
    }

    def __init__(self):
        self.config = self.defaults
