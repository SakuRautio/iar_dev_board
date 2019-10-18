#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def getConfig() -> dict:
	with open('./scripts/config.json', 'r') as configFile:
		return json.loads(configFile)
