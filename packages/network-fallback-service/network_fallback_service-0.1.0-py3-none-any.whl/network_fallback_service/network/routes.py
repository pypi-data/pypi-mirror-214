import subprocess
import logging

from .devices import NetworkDevice

def get_routes():
	cmd = ["ip", "route", "show"]
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	out, _ = process.communicate()

	# Decode the bytes object to string
	out = out.decode()

	# Split the output into lines
	lines = out.split("\n")
	
	# filter for non-empty lines
	routes = [line for line in lines if line != ""]

	return routes

def get_lowest_metric_default_route():
	routes = get_routes()
	
	# filter for non-empty lines and lines that don't contain "default"
	routes = [line for line in routes if "default" in line]

	current_metric = 4294967295 # highest possible metric, a u32
	current_device = None

	for route in routes:
		fields = route.split()

		# get the metric if it exists
		if "metric" not in fields:
			metric = 0 # no metric means highest priority
		else:
			metric = int(fields[fields.index("metric") + 1])

		if metric < current_metric: # equal metrics are ignored, first route wins
			current_metric = metric
			current_device = fields[fields.index("dev") + 1]

	logging.debug("Determined interface with lowest default metric is: %s", current_device)
	# return the default route with the lowest metric
	return current_device


def add_route_to_host(device: NetworkDevice, host: str):
	if host == "":
		return False
	
	if device.gateway is None:
		cmd = ["ip", "route", "add", host, "dev", device.name]
	else:
		logging.debug("Routing via %s", device.gateway)
		cmd = ["ip", "route", "add", host, "via", device.gateway, "dev", device.name]

	logging.debug("Adding route: %s ...", cmd[3:])
	process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)

	# wait for the process to finish
	if process.wait() == 0:
		logging.debug("Route added successfully")
		return True # route succeeded
	else:
		if device.gateway is None:
			logging.warning("Failed to add route to %s on %s", host, device.name)
		else:
			logging.warning("Failed to add route to %s via %s on %s", host, device.gateway, device.name)
		return False

def add_default_route(device: NetworkDevice):
	return add_route_to_host(device, "default")

def del_route_to_host(device: NetworkDevice, host: str):
	if host == "":
		return False
	
	if device.gateway is None:
		cmd = ["ip", "route", "del", host, "dev", device.name]
	else:
		cmd = ["ip", "route", "del", host, "via", device.gateway, "dev", device.name]

	logging.debug("Removing route: %s ...", cmd[3:])
	process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)

	# wait for the process to finish
	if process.wait() == 0:
		logging.debug("Route removed successfully")
		return True # route succeeded
	else:
		if device.gateway is None:
			logging.warning("Failed to delete route to %s on %s", host, device.name)
		else:
			logging.warning("Failed to delete route to %s via %s on %s", host, device.gateway, device.name)
		return False
	
def del_default_route(device: NetworkDevice):
	return del_route_to_host(device, "default")