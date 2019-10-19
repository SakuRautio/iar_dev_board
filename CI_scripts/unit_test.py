#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import json
import re

from error_code import ErrorCode
import config
import version

def runUnitTests(project: str) -> dict:
	ret = dict()
	ret["ErrorCode"] = ErrorCode.OK
	ret["stdout"] = ""
	generalFile = r"{0}\{0}.UnitTest.general.xcl".format(project)
	driverFile = r"{0}\{0}.UnitTest.driver.xcl".format(project)
	process = subprocess.run([config.configDict["IAR_CSPY_PATH"], "-f", generalFile, "--backend", "-f", driverFile], check=False, capture_output=True, text=True)
	print(process.stdout)
	ret["stdout"] = process.stdout
	if (process.returncode):
		print(process.stderr)
		ret["ErrorCode"] = ErrorCode.OS_FAIL
		return ret
	return ret

def parseUnitTestOutput(output: str) -> dict:
	ret = dict()
	started = False
	for line in output.splitlines():
		if (line == "Unit Tests: Start"):
			started = True
		if (started):
			if (line.startswith("Unit Tests: End")):
				result = line.split("Unit Tests: End. ")[1].replace('\n','')
				successfulTests = int(re.search(r'Success:\d,', result).group(0).replace('Success:','').replace(',',''))
				failedTests = int(re.search(r'Failed:\d,', result).group(0).replace('Failed:','').replace(',',''))
				totalTests = int(re.search(r'Total:\d', result).group(0).replace('Total:','').replace('\r\n',''))
				ret["Total"] = totalTests
				ret["Failed"] = failedTests
				ret["Successful"] = successfulTests
				return ret
	return ret

def main() -> ErrorCode:
	errorCode = ErrorCode.OK
	branch = version.getCurrentBranch()
	if (branch == ""):
		return ErrorCode.GIT_FAIL
	unitTestStatus = dict()
	unitTestStatus["ErrorCode"] = ErrorCode.OK
	unitTestStatus["stdout"] = ""
	timestampStart = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	for project in config.configDict["Branches"][branch]["Unit test"]:
		unitTestStatus = runUnitTests(project)
		if (unitTestStatus["ErrorCode"].value):
			return unitTestStatus["ErrorCode"]
	timestampStop = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	parsedUnitTestOutput = parseUnitTestOutput(unitTestStatus["stdout"])
	if (not parsedUnitTestOutput):
		print("Error: Could not parse unit test output!")
		return ErrorCode.PARSE_FAIL
	parsedUnitTestOutput["Start"] = timestampStart
	parsedUnitTestOutput["Stop"] = timestampStop
	with open('unit_tests_results.json', 'w+') as unitTestsResultFile:
		json.dump(parsedUnitTestOutput, unitTestsResultFile, indent=2)
	return errorCode

if __name__ == '__main__':
	errorCode = main()
	sys.exit(errorCode.value)
