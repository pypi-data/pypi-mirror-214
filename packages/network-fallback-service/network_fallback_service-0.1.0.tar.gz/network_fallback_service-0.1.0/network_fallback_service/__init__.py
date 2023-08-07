default_config_path = "/etc/network-fallback.d/default.conf"

def default_entry():
	print("You are looking for something else. Try either:")
	print("'network-fallback-launch' to launch the service")
	print("'network-fallback-config' to create a new configuration\n")

	print("Alternatively, you can point the service to an existing configuration by \nediting the launch command in '/etc/systemd/system/network-fallback.service'")


if __name__ == '__main__':
	default_entry()