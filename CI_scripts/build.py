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
	buildBackupPath = config.configDict["Build backup path"]
	buildBackupPath = os.path.join(buildBackupPath, latestTag)
	if (not os.path.exists(buildBackupPath)):
		try:
			os.makedirs(buildBackupPath)
		except:
			print("Could not create directory {0}".format(buildBackupPath))
			return ErrorCode.OS_FAIL
	buildBackupPath = os.path.join(buildBackupPath, project)
	if (not os.path.exists(buildBackupPath)):
		try:
			os.makedirs(buildBackupPath)
		except:
			print("Could not create directory {0}".format(buildBackupPath))
			return ErrorCode.OS_FAIL
	buildBackupPath = os.path.join(buildBackupPath, configuration)
	if (not os.path.exists(buildBackupPath)):
		try:
			os.makedirs(buildBackupPath)
		except:
			print("Could not create directory {0}".format(buildBackupPath))
			return ErrorCode.OS_FAIL
	buildBackupPath = os.path.join(buildBackupPath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
	if (not os.path.exists(buildBackupPath)):
		try:
			os.makedirs(buildBackupPath)
		except:
			print("Could not create directory {0}".format(buildBackupPath))
			return ErrorCode.OS_FAIL
	print("Copying binary to {0}".format(buildBackupPath))
	shutil.copy2(binaryPath, buildBackupPath)
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
