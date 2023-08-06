from setuptools import setup

setup(
	name='Albumize',
	version='1.2',
	author='Winstang',
	author_email='Winstang@hotmail.com',
	entry_points={
		'console_scripts': [
			'Albumize=Albumize:CLI'
		]
	},
)
