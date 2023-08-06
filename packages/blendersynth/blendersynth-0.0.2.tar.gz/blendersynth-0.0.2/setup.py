from setuptools import setup, find_packages, Extension

setup(
	name='blendersynth',
	version='0.0.2',
	packages=find_packages(include=['blendersynth', 'blendersynth.*']),
)