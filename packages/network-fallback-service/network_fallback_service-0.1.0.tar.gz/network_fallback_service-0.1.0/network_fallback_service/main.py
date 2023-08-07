import configparser
import logging
import time
import argparse
import os

from .network import Manager

from . import default_config_path

def main():
	config = configparser.ConfigParser()

	parser = argparse.ArgumentParser(description='Fallback to working network interfaces')
	parser.add_argument("-c", "--config", help = "Path to configuration file")

	args = parser.parse_args()

	if args.config is not None:
		config.read(args.config)
	else:
		config.read(default_config_path)


	if config.getboolean('system', 'debugLogs', fallback=False):
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	manager = Manager(config=config)

	manager.start_check_loop()
	
	interval = config.getint('system', 'interval', fallback=60)
	try:
		while True:
			time.sleep(interval)  # Keep the main thread alive
	except KeyboardInterrupt:
		manager.stop_check_loop()  # Stop the job when the user interrupts the program


if __name__ == '__main__':
	main()