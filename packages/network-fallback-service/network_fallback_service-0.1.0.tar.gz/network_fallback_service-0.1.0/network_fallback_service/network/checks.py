import subprocess
from typing import Callable
import configparser

import logging

from .devices import NetworkDevice
from .routes import (
	get_routes,
	add_route_to_host,
	del_route_to_host,
)

default_remote_host = "8.8.8.8"

class DeviceCheckSuite:
	def __init__(self, config: configparser.ConfigParser):
		self._checks = []
		
		check_sections = [section for section in config.sections() if section.startswith("check.")]
		for check in check_sections:
			check_type = config[check].get('type', None)
			make_route = config[check].getboolean('makeRoute', False)
			check_host = config[check].get('host', default_remote_host)
			
			if check_type == "ping":
				logging.debug("Defining ping check to %s", check_host)
				check = ConnectionCheck(check=ping_check, make_route=make_route, host=check_host)
			elif check_type == "curl":
				logging.debug("Defining curl check to %s", check_host)
				check = ConnectionCheck(check=curl_check, make_route=make_route, host=check_host)
			else:
				raise RuntimeError("Unknown check type: " + check_type)
			
			self._checks.append(check)

	def check(self, device: NetworkDevice):
		if device.is_up() == False:
			logging.debug("%s interface is down, trying to bring it up ...", device.name)
			if device.bring_up():
				logging.debug("%s interface brought up successfully", device.name)
			else:
				logging.debug("Couldn't bring up %s interface", device.name)
				return False

		for case in self._checks:
			
			logging.debug("Checking connection to %s using %s", case.get_host(), case.get_name())

			if case.check(device):
				logging.debug("%s passed test: %s", device.name, case.get_name())
				return True
			else:
				logging.debug("%s failed test: %s", device.name, case.get_name())
				return False


class ConnectionCheck:
	def __init__(self, make_route: bool, host: str, check: Callable[[NetworkDevice], str]):
		self._make_route = make_route
		self._host = host
		self._check = check
		logging.debug("Defined new check. Host: %s, Make route: %s", self._host, self._make_route)
	
	def check(self, device: NetworkDevice):
		if self._make_route:
			if check_explicit_route(device, self._host):
				return self._check(self._host, device.name)	
			else:
				add_route_to_host(device, self._host)
				rt = self._check(self._host, device.name)
				del_route_to_host(device, self._host)
				return rt

		else: 
			return self._check(self._host, device.name)
		
	def get_name(self):
		return self._check.__name__
	
	def get_host(self):
		return self._host






def ping_check(host: str, interface: str):
	logging.debug("Checking ping to %s on %s ...", host, interface)
	cmd = ["ping", "-c1", "-I", interface, "-W3", host]
	response = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)

	if response.wait() == 0:
		return True
	else:
		logging.debug("Ping failed with exitcode: %d", response.returncode)
		return False
	
def curl_check(host: str, interface: str):
	logging.debug("Checking curl %s on %s ...", host, interface)
	cmd = ["curl", "--interface", interface, "http://{0}".format(host)]
	response = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)

	if response.wait() == 0:
		return True
	else:
		logging.debug("Curl failed with exitcode: %d", response.returncode)
		return False






def check_explicit_route(device: NetworkDevice, host):
	routes = get_routes()

	# filter for routes matching the given host
	routes = [route for route in routes if host in route]

	# filter for routes matching the given device
	routes = [route for route in routes if device.name in route]

	# filter for routes matching the given gateway
	if device.gateway != None:
		routes = [route for route in routes if device.gateway in route]

	# return true if there is a route matching the specification
	return len(routes) > 0

def has_default_route(device: NetworkDevice):
	routes = get_routes()

	# filter for routes matching the given device
	routes = [route for route in routes if device.name in route]

	# filter for routes matching the given gateway
	if device.gateway != None:
		routes = [route for route in routes if device.gateway in route]

	# filter for routes with host "default"
	rt = [route for route in routes if "default" or "0.0.0.0" in route]
	
	# return true if there is a route matching the specification
	return len(rt) > 0