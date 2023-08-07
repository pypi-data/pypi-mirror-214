import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler

import configparser

from .checks import (
	DeviceCheckSuite,
  has_default_route
)

from .devices import NetworkDevice

from .device_types.ifupdown import bring_up	as ifupdown_bring_up
from .device_types.ifupdown import bring_down as ifupdown_bring_down
from .device_types.NetworkManager import bring_up as network_manager_bring_up
from .device_types.NetworkManager import bring_down as network_manager_bring_down

from .routes import *

class Manager:
	def __init__(self, config: configparser.ConfigParser):
		
		# if config.sections doesn't contain at least one section starting with "iface.", and at least one section starting with "check.", raise an error
		if not any(section.startswith("iface.") for section in config.sections()):
			raise RuntimeError("No interfaces defined in configuration file")
		if not any(section.startswith("check.") for section in config.sections()):
			raise RuntimeError("No checks defined in configuration file")

		self._fail_count = 0
		self._retry_limit = config.getint('checks', 'retryLimit', fallback=5)
		logging.debug("Retry limit set to %d", self._retry_limit)
		self._check_interval = config.getint('checks', 'interval', fallback=60)
		logging.debug("Check interval set to %d", self._check_interval)

		self._scheduler = None

		self._current_iface = None
		self._primary_iface = None
		self._secondary_ifaces = []
		self._change_made = True

		self._check_suite = DeviceCheckSuite(config)

		iface_sections = [section for section in config.sections() if section.startswith("iface.")]
		## create the Device objects from the config file
		for iface in iface_sections:
			name = removestrprefix(iface, "iface.")
			iface_type = config[iface].get('type', 'NetworkManager')
			gateway = config[iface].get('gateway', None)
			persistent = config[iface].getboolean('persistent', True)
			primary = config[iface].getboolean('primary', False)

			if iface_type == "ifupdown":
				dev = NetworkDevice(bring_up_strategy=ifupdown_bring_up, bring_down_strategy=ifupdown_bring_down, name=name, gateway=gateway, persistent=persistent)
			elif iface_type == "NetworkManager":
				dev = NetworkDevice(bring_up_strategy=network_manager_bring_up, bring_down_strategy=network_manager_bring_down, name=name, gateway=gateway, persistent=persistent)

			if primary:
				if self._primary_iface is None:
					self._primary_iface = dev
				else:
					raise RuntimeError("Multiple primary interfaces defined in configuration file")
			else:
				self._secondary_ifaces.append(dev)

	def _log_on_state_change(self, log):
		if self._change_made:
			logging.info(log)
			self._change_made = False
		else:
			logging.debug(log)

	def update_current_interface(self):
		logging.debug("Updating current interface ...")
		dev_name = get_lowest_metric_default_route()
		if dev_name is None:
			return False

		for iface in [self._primary_iface] + self._secondary_ifaces:
			if dev_name == iface.name:
				self._current_iface = iface
				return True

		raise RuntimeError("Default route does not match any configured interfaces")
	
	# def get_current_iface(self):
	# 	self.update_current_interface()
	# 	return self._current_iface

	# def iface_is_up(self, dev: NetworkDevice):
	# 	return self._check_suite.check(dev)
	
	def check_device(self, dev: NetworkDevice):
		return self._check_suite.check(dev)
	

	def _swap_if_its_good(self, dev: NetworkDevice):
		if self.check_device(dev):
			logging.info("Swapping to '%s'", dev.name)
			if self.swap_to_interface(dev):
				logging.debug("Swap to '%s' successful", dev.name)
				self._fail_count = 0
				self._change_made = True
				self._current_iface = dev
				return True
			else:
				logging.warning("Swap to '%s' failed", dev.name)
		return False
	
	def _routine_check(self):
		if not self.update_current_interface():
			logging.warning("No default route found, you arent connected to the internet!")
			# bring up the primary interface
			self._primary_iface.bring_up()

			logging.debug("Brought up the primary interface")
			
			if self._fail_count >= self._retry_limit:
				logging.info("Failed to find a working interface %d times in a row, rebooting ...", self._fail_count)
				## No working interfaces could be found, so reboot once the limit is reached
				os.system("reboot")
				exit(1)
			else:
				self._fail_count += 1

			return

		found_working = False

		if self.check_device(self._current_iface):
			
			self._log_on_state_change( "Device %s is working" % self._current_iface.name ) 
			
			found_working = True
			if self._primary_iface != self._current_iface:
				logging.debug("Testing if we can swap back to the primary interface '%s'", self._primary_iface.name)
				# if currently using a secondary interface, test if the primary is working so you can swap back to it
				self._swap_if_its_good(self._primary_iface)
		
		else: ## current interface is down
			if self._current_iface != self._primary_iface:
				## current interface is a secondary interface
				logging.info("Secondary device \'%s\' has failed. Rechecking the primary ...", self._current_iface.name)

				if not self._swap_if_its_good(self._primary_iface):
					## primary is still down, swap to a different secondary interface
					logging.info("Primary is still down. Testing other secondary devices ...")
					other_secondarys = [iface for iface in self._secondary_ifaces if iface != self._current_iface]
					for iface in other_secondarys:
						if self._swap_if_its_good(iface): found_working = True

			else:
				## current interface is primary interface
				## primary interface is down, swap to a secondary interface
				logging.info("Primary device has failed. Testing secondary devices ...")
				for iface in self._secondary_ifaces:
					if self._swap_if_its_good(iface): found_working = True

		if found_working: self._fail_count = 0
		else: self._fail_count += 1

		if self._fail_count >= self._retry_limit:
			logging.info("Failed to find a working interface %d times in a row, rebooting ...", self._fail_count)
			## No working interfaces could be found, so reboot once the limit is reached
			os.system("reboot")


	def start_check_loop(self):
		# mask logging messages from apscheduler
		if not logging.getLogger().isEnabledFor(logging.DEBUG):
			logging.getLogger('apscheduler').setLevel(logging.WARNING)
		else:
			logging.getLogger('apscheduler').setLevel(logging.INFO)

		self._scheduler = BackgroundScheduler()
		self._scheduler.add_job(self._routine_check, 'interval', seconds=self._check_interval)
		self._scheduler.start()
		logging.info("Started check job loop")

	def stop_check_loop(self):
		self._scheduler.remove_all_jobs()
		self._scheduler.shutdown()
		logging.info("Stopped check job loop")

	def swap_to_interface(self, target: NetworkDevice):
		if self._current_iface == target:
			logging.debug("Tried swapping to an interface already in use")
			return True

		if target.is_up() == False:
			logging.debug("Interface isn't up, trying to bring it up ...")
			
			if target.bring_up() == False:
				logging.warning("Failed to bring interface up while swapping to it")
				return False

		if has_default_route(target):
			logging.debug("Interface already has a default route, only deleting the current interfaces route ...")
			del_default_route(self._current_iface)
		else:
			logging.debug("Adding default route for %s ...", target.name)
			
			del_default_route(self._current_iface)

			if not add_default_route(target):
				logging.warning("Failed to make a default route for %s", target.name)

			if self.check_device(target):
				return True
			else:
				logging.debug("%s failed checks while trying to swap to it, so it was aborted", target.name)
				del_default_route(target)
				add_default_route(self._current_iface)

		return False



def removestrprefix(A: str, prefix: str) -> str:
	if A.startswith(prefix):
		return A[len(prefix):]
	else:
		return A[:]
