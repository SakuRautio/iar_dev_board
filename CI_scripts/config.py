#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

configDict = dict()
with open('./CI_scripts/config.json', 'r') as configFile:
	configDict = json.load(configFile)
