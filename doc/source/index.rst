JenkinsAPI
==========

Jenkins is the market leading continuous integration system, originally created by Kohsuke Kawaguchi. This API makes Jenkins even easier to use by providing an easy to use conventional python interface.

Jenkins (and It's predecessor Hudson) are fantastic projects - but they are somewhat Java-centric. Thankfully the designers have provided an excellent and complete REST interface. This library wraps up that interface as more conventional python objects in order to make most Jenkins oriented tasks simpler.

This library can help you:

 * Query the test-results of a completed build
 * Get a objects representing the latest builds of a job
 * Search for artifacts by simple criteria
 * Block until jobs are complete
 * Install artifacts to custom-specified directory structures
 * Username/password auth support for jenkins instances with auth turned on
 * Search for builds by subversion revision
 * Add, remove and query jenkins slaves

Important links
===============

Project source code: github: https://github.com/salimfadhley/jenkinsapi

Releases: http://pypi.python.org/pypi/jenkinsapi

This documentation: http://packages.python.org/jenkinsapi/

Installation
============

Egg-files for this project are hosted on PyPi. Most Python users should be able to use pip or distribute to automatically install this project.

Most users can do the following:

    pip install jenkinsapi

Project Authors
===============

 * Salim Fadhley (sal@stodge.org) 
 * Ramon van Alteren (ramon@vanalteren.nl) 
 * Ruslan Lutsenko (ruslan.lutcenko@gmail.com) 

Plus many others, please see the README file for a more complete list of contributors and how to contact them.

Extending and Improving JenkinsAPI
==================================

JenkinsAPI is a pure-python project and can be improved with almost any programmer's text-editor or IDE. I'd recomend the following project layout which has been shown to work with both SublimeText2 and Eclipse/PyDev

 * Make sure that pip and virtualenv are installed on your computer. On most Linux systems these can be installed directly by the OS package-manager. 
 * Create a new virtualenv for the project::
 	virtualenv jenkinsapi
 * Change to the new directory and check out the project code into the **src** subdirectory
 	cd jenkinsapi
 	git clone https://github.com/salimfadhley/jenkinsapi.git src
 * Activate your jenkinsapi virtual environment::
 	cd bin
 	source activate
 * Install the jenkinsapi project in 'developer mode' - this step will automatically download all of the project's dependancies::
 	cd ../src
 	python setup.py develop
 * Test the project - this step will automatically download and install the project's test-only dependancies. Having these installed will be helpful during development::
 	python setup.py test
 * Set up your IDE/Editor configuration - the **misc** folder contains configuration for Sublime Text 2. I hope in time that other developers will contribute useful configurations for their favourite development tools.

Testing
-------

The project maintainers welcome any code-contributions. Please conside the following when you contribute code back to the project:

 * All contrubutions should come as github pull-requests. Please do not send code-snippets in email or as attachments to issues.
 * Please take a moment to clearly describe the intended goal of your pull-request.
 * Please ensure that any new feature is covered by a unit-test

Package Contents
================

.. toctree::
   jenkinsapi
   jenkinsapi.command_line
   jenkinsapi.utils
   modules
	
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

