import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="jdbl",
	version="0.1.1",
	author="lingchuL, Junyi Wang",
	author_email="2938843848@qq.com",
	description="A json based database library, RAM running and including basic read-write lock.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/lingchuL/py-jdb",
	packages=setuptools.find_packages(),
	install_requires=['appdirs==1.4.1'],
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
)
