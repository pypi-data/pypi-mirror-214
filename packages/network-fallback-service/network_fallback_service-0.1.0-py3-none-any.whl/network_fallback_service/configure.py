import configparser
import re
import os
import netifaces

def check_sudo():
  if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again using 'sudo'. Exiting...")

def yes_no_input(prompt, default=None):
  while True:
    value = input(prompt).lower().strip()
    if value in ['yes', 'no', 'y', 'n', '']:
      if (value == 'yes') or (value == 'y'):
        return True
      elif (value == 'no') or (value == 'n'):
        return False
      elif value == '' and default != None:
        return default
    print("Invalid input. Please enter 'yes' or 'no'.")

def ip_input(prompt):
  while True:
    ip = input(prompt)
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
      return ip
    print("Invalid IP address. Please enter a valid IP address.")

def input_validation(prompt, valid_input_list):
  while True:
    value = input(prompt).strip()
    if value in valid_input_list:
      return value
    print("Invalid input. Please enter one of the following: {0}.".format(', '.join(valid_input_list)))


def input_interface_validate(prompt):
  while True:
    value = input(prompt).strip()
    if value in netifaces.interfaces():
      return value
    print("Interface not found. These are the existing interfaces: {0}.".format(', '.join(netifaces.interfaces())))
    if yes_no_input("Override? (n): ", False):
      return value


## written mostly by ChatGPT
def interactive_config_maker():
  check_sudo()

  config = configparser.ConfigParser()

  print('')

  # ask for primary interface
  primary_iface = input_interface_validate("Enter the primary network interface: ")
  config["iface."+primary_iface] = {'primary': 'true', 'persistent': 'true'}
  config["iface."+primary_iface]['type'] = input_validation("Enter the interface type \n(accepted values are 'ifupdown' or 'NetworkManager'): ", ['ifupdown', 'NetworkManager'])
  if yes_no_input("Does {0} use a gateway? (y/n): ".format(primary_iface)):
    config["iface."+primary_iface]['gateway'] = ip_input("Enter the IP of the gateway for the primary interface: ")

  if yes_no_input("\nAdd a secondary network interface? (y): ", True):
    secondary_iface = input_interface_validate("Name of the network interface: ")
    config["iface."+secondary_iface] = {'persistent': 'true'}
    config["iface."+secondary_iface]['type'] = input_validation("Enter the interface type \n(accepted values are 'ifupdown' or 'NetworkManager'): ", ['ifupdown', 'NetworkManager'])
    if yes_no_input("Does {0} use a gateway? (y/n): ".format(secondary_iface)):
      config["iface."+secondary_iface]['gateway'] = ip_input("Enter the IP of the gateway for {0}: ".format(secondary_iface))

  # ask for secondary interfaces
  while yes_no_input("\nAdd another secondary network interface? (y/n): "):
    secondary_iface = input_interface_validate("Name of the network interface: ")
    config["iface."+secondary_iface] = {'persistent': 'true'}
    config["iface."+secondary_iface]['type'] = input_validation("Enter the interface type \n(accepted values are 'ifupdown' or 'NetworkManager'): ", ['ifupdown', 'NetworkManager'])
    if yes_no_input("Does {0} use a gateway? (y/n): ".format(secondary_iface)):
      config["iface."+secondary_iface]['gateway'] = ip_input("Enter the IP of the gateway for {0}: ".format(secondary_iface))

  print('\nWe will now define the connectivity checks that will be run using ping or curl.')
  # ask for checks
  while True:
    check_name = input("Name for the new connectivity check (can be anything): ")
    check_name = re.sub('[^A-Za-z0-9]+', '', check_name)
    config["check."+check_name] = {}
    config["check." + check_name]['type'] = input_validation("Enter the check type \n(accepted values are 'ping' or 'curl'): ", ['ping', 'curl'])
    
    while True:
      host = input("Enter the host to check for: ")

      if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', host):
        if yes_no_input("You havent provided an IPv4 address. Shall we try to resolve one from the address you gave? (y): ", True):
          host = os.popen('dig +short {0}'.format(host)).read().strip()

          if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', host):
            print("Couldnt resolve IP address. Please try again ...")
            continue
          elif not yes_no_input("Resolved to {0} . Is this correct? (y): ".format(host), True):
            continue
        else:
          continue
      
      config["check." + check_name]['host'] = host
      break
    
    # if yes_no_input("Does this check require a temporary route to be created to reach the host? (y): ", True):
    config["check." + check_name]['makeRoute'] = 'true'

    if not yes_no_input("\nDefine another connectivity check? (y/n): "):
      break
  
  # use default values
  config['checks'] = {'interval': '30', 'retryLimit': '6'}

  # system settings default values
  config['system'] = {'debugLogs': 'false'}
  

  # write to configuration file
  config_name = re.sub('[^A-Za-z0-9]+', '', input("\nEnter the name for the new configuration (default is 'default'): ") )
  if not config_name:
    config_name = 'default.conf'
  else:
    config_name += '.conf'

  config_path = '/etc/network-fallback.d/{0}'.format(config_name)

  # Ensure the directory exists; create it if necessary
  os.makedirs('/etc/network-fallback.d', exist_ok=True)

  with open(config_path, 'w') as configfile:
    config.write(configfile)

  update_service_file(config_path)

def update_service_file(config_path):
  service_file_path = '/etc/systemd/system/network-fallback.service'
  template = """[Unit]
Description=Automatic network interface switching
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/network-fallback-launch --config {0}
Restart=always

[Install]
WantedBy=multi-user.target
"""

  if os.path.exists(service_file_path):
    with open(service_file_path, 'r') as f:
      lines = f.readlines()

    with open(service_file_path, 'w') as f:
      for line in lines:
        if line.startswith('ExecStart='):
          if '--config' in line:
            # Replace existing --config path
            line = re.sub(r'(--config \S+)', '--config {0}'.format(config_path), line)
          else:
            # Append --config path
            line = line.strip() + ' --config {0}\n'.format(config_path)
        f.write(line)
  else:
    with open(service_file_path, 'w') as f:
      f.write(template.format(config_path))


if __name__ == '__main__':
  interactive_config_maker()
