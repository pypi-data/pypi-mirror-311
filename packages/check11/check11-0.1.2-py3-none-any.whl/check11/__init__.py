#!/usr/bin/env python

import requests
import os
import sys
import subprocess
import re
import time
from colorama import Fore
from colorama import Style
from pprint import pprint as ppp

# paths and mods
# PARENT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(PARENT)
# from check11.base_test import BaseTest

VERSION = '0.1.2'
APP_NAME = 'check11'
BASEURL = 'https://cpnits.com/check11'
# BASEURL = 'http://127.0.0.1:5000'
MAXSIZE = 1024 * 1024

def auth():
	print('authenticate and authorize')
	# first authenticate as Git user
	# then authorize this app for making, updating repo: cpnits.
	
	# store auth data in client dir
	# make sure check11 does not work if no auth	

def help(short=True):
	if short:
		print(f"Type {Fore.BLUE}{Style.BRIGHT}check11 -h{Style.NORMAL}{Fore.RESET} for a brief howto.{Style.RESET_ALL}")
	else:
		print(f"{Style.BRIGHT}How to use check11: \n\t{Fore.LIGHTRED_EX}{Style.BRIGHT}check11 assignmentname /absolute/path/to/dir/with/assignment/ {Style.RESET_ALL}")
		print(f"\tor {Fore.LIGHTRED_EX}{Style.BRIGHT}check11 assignmentname relative/path/with/assignment/ {Style.RESET_ALL}")
		print(f"\tor in current working directory: {Fore.LIGHTRED_EX}{Style.BRIGHT}check11 assignmentname -c {Style.RESET_ALL}")
		print()
		print(f"{Style.BRIGHT}For help{Style.NORMAL}: {Fore.LIGHTRED_EX}{Style.BRIGHT}check11 -h {Style.RESET_ALL}")
		print()
		print(f"Additional arg for no traceback: {Fore.LIGHTRED_EX}{Style.BRIGHT} --t{Style.RESET_ALL}")
		print(f"Additional arg for errors only: {Fore.LIGHTRED_EX}{Style.BRIGHT} --e{Style.RESET_ALL}")
		print(f"Additional arg for clearing prompt: {Fore.LIGHTRED_EX}{Style.BRIGHT} --p{Style.RESET_ALL}")
		print(f"Combined args for no traceback and errors only: {Fore.LIGHTRED_EX}{Style.BRIGHT} --te{Style.RESET_ALL}")
		print()
		print(f"Example (assignment in current dir, errors only, no traceback, clear prompt): \n\t{Fore.LIGHTRED_EX}{Style.BRIGHT}check11 assignmentname --etp -c{Style.RESET_ALL}")
		print(f"Example (assignment in relative dir assignment, clear prompt): \n\t{Fore.LIGHTRED_EX}{Style.BRIGHT}check11 assignmentname --p assignment/{Style.RESET_ALL}")


def read_cmd() -> dict:
	# read the commands in versatile way:
	# check11 assignmentname -c or -C or -current ==> for assignment == current working dir
	# check11 assignmentname-h or -H or -help ==> for help
	# check11 assignmentname /abs/path/to/assignment/dir
	# check11 assignmentname --t /abs/path/to/assignment/dir ==> no traceback 
	# check11 assignmentname --e /abs/path/to/assignment/dir ==> errors only
	no_trace = False
	errors_only = False
	clear_prompt = False
	no_report = False
	apath = None
	counter = 0
	aname = None
	
	for i in range(len(sys.argv)):
		a = sys.argv[i].strip()
		
		# skip program call
		if i == 0:
			counter += 1
			continue
		
		# help, ignore the rest
		if a.lower() in ['-h', '-help']:
			help(short=False)
			sys.exit()
			
		# auth, ignore the rest
		if a.lower() in ['-a', '-auth']:
			auth()
			sys.exit()	
		
		# name of the assignment
		if i == 1:
			aname = sys.argv[i].lower().strip()
			counter += 1
			continue

		## The rest of the args can come in any order
		if a.startswith(('/', '~/',)):
			if not apath is None:
				# two paths?
				help()
				sys.exit()
			if os.path.isabs(a):
				apath = a
				counter += 1
				continue
			else:
				help()
				sys.exit()				
		
		# relative path can be any word not starting with
		if not a.startswith(("-", "/", "~",)):
			if not apath is None:
				# two paths?
				help()
				sys.exit()
			apath = os.path.abspath(a)
			counter += 1
		
		if a.startswith('--'):
			try:
				extra_args = a.split('--')[1]
			except:
				# no args after --
				help()
				sys.exit()
			if not extra_args.isalpha():
				help()
				sys.exit()				
			if 't' in extra_args:
				no_trace = True
			if 'e' in extra_args:
				errors_only = True
			if 'p' in extra_args:
				clear_prompt = True
			if 'r' in extra_args:
				no_report = True			
			counter += 1
				
	# end sys.argv for
	if len(sys.argv) != counter:
		help()
		sys.exit()
	if aname is None:
		help()
		sys.exit()	
		
	# path might be omitted
	if apath is None:
		apath = os.getcwd()

	# print('INPUT', apath, aname, no_trace, errors_only, clear_prompt, no_report)
	return apath, aname, no_trace, errors_only, clear_prompt, no_report
	

class TestAssignment:
	# this object reads manages a dir with assignments
	def __init__(self, path: str, aname: str, no_trace: bool, errors_only: bool, clear_prompt: bool, no_report: bool):
		self._git_alias = self.get_git_alias()
		if self._git_alias is None:
			print("No valid GIT account.")
			return False
		self._no_trace = no_trace
		self._errors_only = errors_only
		self._clear_prompt = clear_prompt
		self._no_report = no_report
		self._this_path = path
		self._assignment = aname
		self._all_test_mods = list()
		self.run()


	# removes colorama from report file
	def unescape(self, s: str) -> str:
		ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		result = ansi_escape.sub('', s)
		return result		

	# changes nam in safe version
	def safename(self, erin: str):
		erin = str(erin)
		return re.sub(r'[^a-zA-Z0-9_\.]', '', erin, flags=re.I|re.M).lower()


	# prints report to prompt
	def print_report(self):
		for line in self.results:
			print(line)


	# get git info from project
	def get_git_alias(self) -> str|None:
		try:
			res = subprocess.run(["git", "config", "user.email"], stdout=subprocess.PIPE)
			git_data = res.stdout.strip().decode()
			git_alias = git_data.split('@')[0].strip()
			# print('GET GIT DATA', git_alias)
			return git_alias
		except:
			return None

	
	# get permission for testing AND VERSION
	def remote_get_permission(self) -> int:
		url = f"{BASEURL}/permission/{self._git_alias}/{self._assignment}"
		try:
			r = requests.get(url)
			code = int(r.status_code)
			rj = r.json()
			print(rj)
			version = rj['r']['version']
			permission = rj['r']['permission']
		except:
			print(f"{Fore.LIGHTRED_EX}{self._assignment} is not a testable assignment --status [211].{Style.RESET_ALL}")
			return False
		
		if code == 200:
			if version != VERSION:
				print(f"{Fore.LIGHTRED_EX}Check11 is in version {version}. You are running version {VERSION}. Download a new version with {Style.BRIGHT}pip install check11 --upgrade.{Style.RESET_ALL}")
				return False
			
			if permission != self._git_alias:
				print(f"{Fore.LIGHTRED_EX}Your github alias {self._git_alias} does not have access to Check11 --status [{code}].{Style.RESET_ALL}")
				return False
			
			return True
			
		elif code == 401:
			print(f"{Fore.LIGHTRED_EX}Your github alias {self._git_alias} does not have access to Check11 --status [{code}].{Style.RESET_ALL}")
			return False
		elif code == 403:
			print(f"{Fore.LIGHTRED_EX}It looks like the Check11 server is down. Try again later --status [{code}].{Style.RESET_ALL}")
			return False
		else:
			print(f"{Fore.LIGHTRED_EX}{self._assignment} is not a testable assignment --status [{code}].{Style.RESET_ALL}")
			return False		
	
	
	# retreive info about assignment and testable files
	def get_about_assignment(self) -> bool:
		try:
			aboutmod = __import__('about')
			self._allowed_filenames = aboutmod.allowed_filenames()	
		except Exception as e:
			print(f"{e} = {about_path}")
			return False			
		return True
	
	
	# find the user files for testing
	def get_local_filenames(self):
		files = list()
		for f in os.listdir(self._this_path):
			fpath = os.path.join(self._this_path, f)
			if not os.path.isfile(fpath):
				continue
			if not f in self._allowed_filenames:
				continue
			files.append(f)
		self._found_filenames = files
	
	# store full report in user folder
	def local_user_store_report(self):
		s = ""
		for r in self._full_report:
			r = self.unescape(r)
			s += f"{r}\n"
			
		path = os.path.join(self._this_path, f"{self._assignment}.log")
		with open(path, "w") as fp:
			fp.write(s)
		return True
	
	# upload full_reports
	def remote_upload_reports(self):
		target_url = f"{BASEURL}/report/{self._git_alias}/{self._assignment}"
		path = os.path.join(self._this_path, f"{self._assignment}.log")
		with open(path, 'r') as fp:
			s = fp.read()
		try:
			response = requests.post(
				target_url,
				json={"report": s},
			)
		except Exception as e:
			print(e)
			pass
		# no need for output
		# return response.status_code == 200
	
	
	
	
	# put all relevant mods in dict
	def get_all_mods(self):
		
		# sys.path.insert(0, self._test_mod_path)	
		# has been set earlier
		
		self._all_mods = dict()
		for f in list(self._found_filenames):
			fn = f.replace('.py', '')
			fnn = f"test_{fn}"			
			try:
				mod = __import__(fnn)
				self._all_mods[fn] = [mod, None]
			except Exception as e:
				print(f"{Fore.LIGHTRED_EX}Error in {Style.BRIGHT}{f}{Style.NORMAL}:\n\t{e} {Style.RESET_ALL}")
				self._all_mods[fn] = [None, None]
		# remove path to scripts from sys path
		sys.path.remove(self._test_mod_path)	
	
		# now import all user_mods
		# place path to user scripts dir in sys path
		sys.path.insert(0, self._this_path)
		for f in list(self._found_filenames):
			fn = f.replace('.py', '')
			fnn = fn			
			try:
				mod = __import__(fnn)
				self._all_mods[fn][1] = mod
			except Exception as e:
				print(f"{Fore.LIGHTRED_EX}Error in {Style.BRIGHT}{f}{Style.NORMAL}:\n\t{e} {Style.RESET_ALL}")
				self._all_mods[fn][1] = None
		# remove path to scripts from sys path
		sys.path.remove(self._this_path)			
	
	
	# run test in single file within assignment
	def run_single_file(self, fname: str) -> bool:
		
		tmod = self._all_mods[fname][0]
		umod = self._all_mods[fname][1]
		
		# check for single file test class
		if not hasattr(tmod, 'SingleFileTest'):
			print(f"{Fore.CYAN}Testing : {Style.BRIGHT}{self._assignment}.{fname}{Style.NORMAL} failed.{Style.RESET_ALL}")
			return False
		
		sft = tmod.SingleFileTest(
			self._git_alias,
			self._assignment,
			fname,
			self._all_mods[fname],
			self._no_trace, 
			self._errors_only,
		)
		sft.runrun()
		sft.print_report()
		self._full_report.extend(sft.get_report())
	
	
	# gather everything and run tests on all files in assignment
	def run(self) -> bool:
		# get GIT alias from email address
		if self._git_alias is None:
			print("No valid GIT account")
			return False
		
		if self._clear_prompt:
			os.system('cls' if os.name == 'nt' else 'clear')

		# name of project, part of path
		print(f"{Fore.CYAN}Building test for {Style.BRIGHT}{self._assignment}{Style.NORMAL}.{Style.RESET_ALL}")

		# send request to check11 for requested files for this assignment
		if not self.remote_get_permission():
			return False
		
		# check path
		if not os.path.isdir(self._this_path):
			print(f"{Fore.LIGHTRED_EX}The path: {Style.BRIGHT}{self._this_path}{Style.NORMAL} does not exist!{Style.RESET_ALL}")
			return False
		
		# place path to this script dir in sys path
		self._test_mod_path = os.path.join(os.path.dirname(__file__), self._assignment)
		sys.path.insert(0, self._test_mod_path)	
		
		self.get_about_assignment()
		print(f"{Fore.CYAN}Looking for python files {Style.BRIGHT}{self._allowed_filenames}{Style.NORMAL}.{Style.RESET_ALL}")

		# find filenames for testing at user dir
		self.get_local_filenames()
		if len(self._found_filenames) == 0:
			print(f"{Fore.LIGHTRED_EX}No python files found for testing. Maybe {Style.BRIGHT}{self._this_path}{Style.NORMAL} is not the right directory?{Style.RESET_ALL}")
			return False
		print(f"{Fore.CYAN}Python files ready for testing: {Style.BRIGHT}[{', '.join(self._found_filenames)}]{Style.NORMAL}.{Style.RESET_ALL}")
		
		# put all test mods in list
		self.get_all_mods()
		# AT THIS POINT ALL MODS HAVE BEEN LOADED

		self._full_report = list()
		for fn in self._found_filenames:
			fname = fn.replace('.py', '')
			if self._all_mods[fname][0] is None or self._all_mods[fname][1] is None:
				continue
			# run single test per file fn.
			self.run_single_file(fname)

							
		# if no report, skip rest
		if len(self._full_report) == 0 or self._no_report:
			return True
		
		# store full report.log in user folder
		if self.local_user_store_report():
			print(f"{Fore.CYAN}The test report has been saved as {self._assignment}.log{Style.RESET_ALL}.")
		
		# upload full reports 
		self.remote_upload_reports()
		
		
		return True
	
def run():
	# read command line args
	path, an, nt, eo, cp, nr = read_cmd()
	# start test object for assignment
	check11 = TestAssignment(path, an, nt, eo, cp, nr)

# python3 -m build 
# for building the thing
# twine upload dist/*
# for uploading to pypi

# client sometimes needs:
# pip install --upgrade setuptools