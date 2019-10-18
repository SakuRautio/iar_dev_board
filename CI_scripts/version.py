#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess
import argparse

from error_code import ErrorCode

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Version helper')
	parser.add_argument('-g', '--generate', action='store_const', const=True, help='Generate a C header')
	parser.add_argument('-i', '--increment', action='store_const', const=True, help='Increment the version')
	parser.add_argument('-p', '--push', action='store_const', const=True, help='Push the tags to remote')
	args = parser.parse_args()

from error_code import ErrorCode

VERSION_FILE_HEADER = """#ifndef VERSION_H
#define VERSION_H
			
#define SW_VERSION ({0})
			
#endif /* VERSION_H */
"""

def getCurrentBranch() -> str:
	print("Getting current branch")
	process = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=False, text=True, capture_output=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ""
	if (len(process.stdout) < 0):
		return ""
	return process.stdout.replace('\r','').replace('\n','')

def getLatestTag() -> str:
	branch = getCurrentBranch()
	if (branch == ""):
		return ""
	print("Getting latest tags for branch: {0}".format(branch))
	process = subprocess.run(["git", "tag", "-l"], check=False, text=True, capture_output=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ""
	if (len(process.stdout) < 0):
		return ""
	tags = list(map(lambda x: x.replace('\r','').replace('\n',''), process.stdout.split("\r\n")))
	tags = list(filter(lambda x: x.rsplit('-')[-1] == branch, tags))
	print("Tags: {0}".format(tags))
	return tags[-1]

def generateHeaderFile() -> ErrorCode:
	ret = ErrorCode.OK
	latestTag = getLatestTag()
	if (latestTag == ""):
		errorCode = ErrorCode.WTF
		return errorCode
	print("Latest tag: {0}".format(latestTag))
	version = int(latestTag.split('-')[0])
	with open('version.h', 'w+') as versionFile:
		fileContents = VERSION_FILE_HEADER.format(version)
		versionFile.write(fileContents)
	return ret

def incrementTag() -> ErrorCode:
	latestTag = getLatestTag()
	if (latestTag == ""):
		return ErrorCode.GIT_FAIL
	versionNumber = int(latestTag.split('-')[0])
	versionNumber = versionNumber + 1
	newTag = "{0}-{1}".format(versionNumber, ''.join(latestTag.split('-')[1:]))
	process = subprocess.run(["git", "tag", "-a" , newTag, "-m", "Version {0}".format(versionNumber)], check=False, text=True, capture_output=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ErrorCode.WTF
	print("Created a new tag: {0}".format(newTag))
	return ErrorCode.OK

def pushTags() -> ErrorCode:
	process = subprocess.run(["git", "push", "--tags"], check=False, text=True, capture_output=True)
	print(process.stdout)
	if (process.returncode):
		print(process.stderr)
		return ErrorCode.WTF
	print("Pushed new tags")
	return ErrorCode.OK

def main() -> ErrorCode:
	errorCode = ErrorCode.OK
	if (args.generate):
		print("Generating header")
		errorCode = generateHeaderFile()
		if (errorCode.value):
			return errorCode
	if (args.increment):
		print("Incrementing version")
		errorCode = incrementTag()
		if (errorCode.value):
			return errorCode
	if (args.push):
		print("Pushing versions to remote")
		errorCode = pushTags()
		if (errorCode.value):
			return errorCode
	return errorCode

if __name__ == '__main__':
	errorCode = main()
	sys.exit(errorCode.value)
