import netifaces
import subprocess
import logging

from ..devices import NetworkDevice

from ..checks import check_explicit_route

def bring_up(device: NetworkDevice):
  if device.disabled:
    logging.debug("%s is disabled, not bringing it up", device.name)
    return False
  
  if device.name in netifaces.interfaces():
    # Interface is already up
    logging.debug("%s is already up", device.name)
    return True
  
  if check_explicit_route(device, "default") == False:
    ## Bring up the device
    if subprocess.Popen(["nmcli", "dev", "connect", device.name], stdout=subprocess.DEVNULL).wait() != 0:
      logging.warning("nmcli dev connect %s failed!", device.name)
      device.failed_checks += 1
      return False
    ##

  if check_explicit_route(device, "default") == False:
    logging.warning("%s failed to come up OR a default route wasnt made", device.name)
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
  
  logging.debug("Running nmcli dev disconnect %s ...", device.name)
  ## Bring down the device
  if subprocess.Popen(["nmcli", "dev", "disconnect", device.name], stdout=subprocess.DEVNULL).wait() != 0:
    logging.warning("nmcli dev disconnect %s failed!", device.name)
    return False
  ##
  
  return True