#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import shutil

from error_code import ErrorCode
import config
import version

def cleanProject(project: str, configuration: str) -> ErrorCode:
	print("Cleaning: {0} conf: {1}".format(project, configuration))
	process = subprocess.run([config.configDict["IAR_BUILD_PATH"], "{0}\{0}.ewp".format(project), "-clean", "{0}".format(configuration)], check=True, capture_output=True, text=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ErrorCode.IAR_FAIL
	return ErrorCode.OK

def buildProject(project: str, configuration: str) -> ErrorCode:
	print("Building: {0} conf: {1}".format(project, configuration))
	process = subprocess.run([config.configDict["IAR_BUILD_PATH"], "{0}\{0}.ewp".format(project), "-build", "{0}".format(configuration)], check=True, capture_output=True, text=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ErrorCode.IAR_FAIL
	return ErrorCode.OK

def backupProject(project: str, configuration: str) -> ErrorCode:
	print("Backing up: {0} conf: {1}".format(project, configuration))
	latestTag = version.getLatestTag()
	if (latestTag == ""):
		return ErrorCode.WTF
	binaryPath = r"{0}\{1}\Exe\{0}.bin".format(project, configuration)
	buildPath = config.configDict["Build output path"]
	buildPath = os.path.join(buildPath, latestTag)
	if (not os.path.exists(buildPath)):
		try:
			os.makedirs(buildPath)
		except:
			print("Could not create directory {0}".format(buildPath))
			return ErrorCode.OS_FAIL
	buildPath = os.path.join(buildPath, project)
	if (not os.path.exists(buildPath)):
		try:
			os.makedirs(buildPath)
		except:
			print("Could not create directory {0}".format(buildPath))
			return ErrorCode.OS_FAIL
	buildPath = os.path.join(buildPath, configuration)
	if (not os.path.exists(buildPath)):
		try:
			os.makedirs(buildPath)
		except:
			print("Could not create directory {0}".format(buildPath))
			return ErrorCode.OS_FAIL
	buildPath = os.path.join(buildPath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
	if (not os.path.exists(buildPath)):
		try:
			os.makedirs(buildPath)
		except:
			print("Could not create directory {0}".format(buildPath))
			return ErrorCode.OS_FAIL
	shutil.copy2(binaryPath, buildPath)
	return ErrorCode.OK

def main() -> ErrorCode:
	errorCode = ErrorCode.OK
	branch = version.getCurrentBranch()
	if (branch == ""):
		return ErrorCode.GIT_FAIL
	for configuration in config.configDict["Configurations"]:
		for project in config.configDict["Branches"][branch]["Build"]:
			errorCode = cleanProject(project, configuration)
			if (errorCode.value):
				return errorCode
			errorCode = buildProject(project, configuration)
			if (errorCode.value):
				return errorCode
			errorCode = backupProject(project, configuration)
			if (errorCode.value):
				return errorCode
	return errorCode

if __name__ == '__main__':
	errorCode = main()
	sys.exit(errorCode.value)
