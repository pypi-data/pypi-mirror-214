import netifaces
import subprocess
import logging
import time

from ..devices import NetworkDevice

def bring_up(device: NetworkDevice):
  if device.disabled:
    logging.debug("%s is disabled, not bringing it up", device.name)
    return False
  
  if device.name in netifaces.interfaces():
    # Interface is already up
    logging.debug("%s is already up", device.name)
    return True
  
  logging.debug("Running ifup %s ...", device.name)
  ## Bring up the device
  if subprocess.Popen(["ifup", device.name], stdout=subprocess.DEVNULL).wait() != 0:
    logging.warning("ifup %s failed!", device.name)
    return False
  ##

  time.sleep(5) # devices need some time to come up after ifup exits
  
  if device.name not in netifaces.interfaces():
    logging.info("%s failed to come up", device.name)
    if device.failed_checks >= 4:
      logging.debug("%s failed to come up 5 times in a row, disabling it", device.name)
      device.disabled = True
    elif not device.persistent:
      device.failed_checks += 1

    return False
  
  device.failed_checks = 0
  return True

def bring_down(device: NetworkDevice):
  if device.name not in netifaces.interfaces():
    return True
  
  logging.debug("Running ifdown %s ...", device.name)
  ## Bring down the device
  if subprocess.Popen(["ifdown", device.name], stdout=subprocess.DEVNULL).wait() != 0:
    logging.warning("ifdown %s failed!", device.name)
    return False
  ##
  
  return True