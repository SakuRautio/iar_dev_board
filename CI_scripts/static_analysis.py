#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import sqlite3
import json

from error_code import ErrorCode
import config
import version

def runStaticAnalysis(project: str, configuration: str) -> ErrorCode:
	print("Static analyzing: {0} conf: {1}".format(project, configuration))
	errorCode = ErrorCode.OK
	projectFile = r"{0}\{0}.ewp".format(project)
	print("CSTAT cleaning")
	process = subprocess.run([config.configDict["IAR_BUILD_PATH"], projectFile, "-cstat_clean", "{0}".format(configuration)], check=False, capture_output=True, text=True)
	print(process.stdout)
	if (process.returncode):
		errorCode = ErrorCode.OS_FAIL
		print(process.stderr)
	print("CSTAT analyzing")
	process = subprocess.run([config.configDict["IAR_BUILD_PATH"], projectFile, "-cstat_analyze", "{0}".format(configuration)], check=False, capture_output=True, text=True)
	print(process.stdout)
	if (process.returncode):
		errorCode = ErrorCode.OS_FAIL
		print(process.stderr)
	return errorCode

def getAnalysisData(project: str, configuration: str) -> dict:
	print("Getting analysis data for: {0} conf: {1}".format(project, configuration))
	databaseFile = r"{0}\{1}\Obj\cstat.db".format(project, configuration)
	connection = sqlite3.connect(databaseFile)
	cursor = connection.cursor()
	query = "SELECT warning_id, property_id, file_name, line_num, column_num, msg, severity FROM warnings"
	cursor.execute(query)
	data = dict()
	data["Project"] = project
	data["Configuration"] = configuration
	warnings = list()
	for row in cursor.fetchall():
		warning = dict()
		warning["warning_id"] = row[0]
		warning["property_id"] = row[1]
		warning["file_name"] = row[2]
		warning["line_num"] = row[3]
		warning["column_num"] = row[4]
		warning["msg"] = row[5]
		warning["severity"] = row[6]
		warnings.append(warning)
	data["Warnings"] = warnings
	connection.close()
	return data

def main() -> ErrorCode:
	errorCode = ErrorCode.OK
	branch = version.getCurrentBranch()
	if (branch == ""):
		return ErrorCode.GIT_FAIL
	wholeAnalysis = dict()
	analysises = list()
	for configuration in config.configDict["Configurations"]:
		configBranch = config.configDict["Branches"][branch]
		for key in configBranch:
			if (key == "Static analysis"):
				for project in configBranch["Static analysis"]:
					errorCode = runStaticAnalysis(project, configuration)
					if (errorCode.value):
						return errorCode
					analysis = getAnalysisData(project, configuration)
					if (analysis):
						analysises.append(analysis)
	wholeAnalysis["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	wholeAnalysis["Analysises"] = analysises
	with open('cstat_results.json', 'w+') as cstatResultsFile:
		json.dump(wholeAnalysis, cstatResultsFile, indent=2)
	return errorCode

if __name__ == '__main__':
	errorCode = main()
	sys.exit(errorCode.value)
