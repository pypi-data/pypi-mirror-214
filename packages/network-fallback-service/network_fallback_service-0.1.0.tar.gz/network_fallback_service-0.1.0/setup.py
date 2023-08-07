from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		install.run(self)
		# PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
		print("\033[91m\nRemember to create a configuration before running!\nIf it doesn't start automatically now, use `sudo network-fallback-config` to configure.\n\033[0m")

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='network_fallback_service',
	version='0.1.0',
	author='Nicholas Hassan',
	description='Fallback to working network interfaces',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=find_packages(),
	install_requires=[
		# List your project dependencies here
		# For example: 'numpy >= 1.20.1'
    'argparse >= 1.4',
    'configparser >= 4.0',
    'apscheduler >= 3.9',
		'netifaces >= 0.11.0'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: POSIX :: Linux",
	],
	python_requires='>=3.5',
	entry_points={
		'console_scripts': [
			'network-fallback-launch=network_fallback_service.main:main',
			'network-fallback-config=network_fallback_service.configure:interactive_config_maker',
			'network-fallback=network_fallback_service.__init__:default_entry'
		],
	},
	cmdclass={
		'install': PostInstallCommand,
	}
)
