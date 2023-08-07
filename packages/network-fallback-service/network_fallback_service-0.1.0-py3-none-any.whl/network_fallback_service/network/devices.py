from typing import Callable
import netifaces

class NetworkDevice:
  def __init__(self, name: str, gateway: str, bring_up_strategy: Callable[[], None], bring_down_strategy: Callable[[], None], persistent: bool = False):
    self.name = name
    self.gateway = gateway
    self.bring_up_strategy = bring_up_strategy
    self.bring_down_strategy = bring_down_strategy
    self.persistent = persistent
    self.disabled = False
    self.failed_checks = 0

  def bring_up(self):
    self.bring_up_strategy(self)
  
  def bring_down(self):
    self.bring_down_strategy(self)

  def is_up(self):
    if self.name in netifaces.interfaces():
      return True
    else:
      return False



