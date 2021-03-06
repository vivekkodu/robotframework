.. include:: <isonum.txt>
.. include:: ../userguide/src/roles.rst

=====================================
  Robot Framework Quick Start Guide
=====================================

| Copyright |copy| Nokia Siemens Networks 2008-2013
| Licensed under the `Creative Commons Attribution 3.0 Unported`__ license

__ http://creativecommons.org/licenses/by/3.0/

.. contents:: Table of Contents
   :depth: 2


Introduction
============

Overview
--------

Robot Framework is a generic keyword-driven test automation framework.
Test cases live in HTML, plain text or TSV (tab-separated values) test
files and make use of keywords implemented in test libraries to drive
the software under test. Because Robot Framework is flexible and
extensible, it is ideally suited to testing complex software with a
variety of interfaces: user interfaces, command line, web services,
proprietary programming interfaces, etc.

Robot Framework is open source software and installation packages,
source code and further documentation is available through
http://robotframework.org. This guide is designed to introduce the
basic concepts of Robot Framework.  For a detailed technical
description, please refer to `Robot Framework User Guide`_.


Installation
------------

A precondition for installing Robot Framework is having Python_ installed.
In addition, to use test libraries written in Java, Jython_ must be
installed. To use this Quick Start Guide, Python is enough.

There are three different ways to install Robot Framework, of which
the most suitable can be chosen. Detailed `installation instructions`_
can be found from the project web pages and installation packages
are available on the `download page`_.

1.  There is a binary installer for Windows platform. It is enough to
    double-click the installer and follow instructions.

2.  On every platform, Robot Framework can be installed from
    source. To install from source, extract the source distribution
    and run command :cli:`python setup.py install`.

3.  If Python package management system `Easy Install`_ is available,
    Robot Framework can be installed by issuing command
    :cli:`easy_install robotframework`. On Windows you also need to
    run :path:`robot_postinstall.py` script manually.

After the framework is installed, it is useful to include the
directory containing start-up scripts in :var:`PATH` environment
variable. On UNIX-like systems this should actually happen
automatically, but on Windows this must be done from ``Control Panel >
System > Advanced > Environment Variables`` by adding e.g.
:path:`C:\\Python25\\Scripts` to :var:`PATH`.

Successful installation can be verified with command :cli:`pybot
--version` which should output something like::

    $ pybot --version
    Robot Framework 2.5.7 (Python 2.6.6 on linux2)


Running this demo
-----------------

This Quick Start Guide also acts as an executable demo. If you are
reading this guide online, you need to first download the
:path:`robotframework-quickstart-<date>.zip` file from the `download
page`_ and extract it somewhere. To run the demo, open a command
prompt, go to the directory where this file (:path:`quickstart.html`)
is located, and then type the following command::

   pybot quickstart.html

The tests in this file will execute and generate the following reports:

:path:`report.html`
   the test results summary
:path:`log.html`
   the test results details
:path:`output.xml`
   the test results in a portable XML format for integration with other tools

Open `report.html`__ (the link works only after this guide has been
executed) in your browser, then click on the links to explore the
results. The :path:`report.html` file links to the :path:`log.html`
file.

__ report.html

There are also a number of command line options that can be used to
control the test execution and generated outputs. Complete list can be
viewed by issuing :cli:`pybot --help`. For example the following
command changes the name of the log file and the name of the top level
test suite::

    pybot --log mylog.html --name My_Fine_Tests quickstart.html

.. Note:: Executing this demo is not possible with :prog:`jybot` start-up script.


Introducing the sample application
----------------------------------

The sample application for this guide is a variation on a classic
login example: it is a command-line based authentication server written
in Python. At the moment, the sample application allows a user to do
three things:

* Create an account with a valid password.
* Log in with a valid user name and password.
* Change the password of an existing account.

The application itself is in the :path:`sut` directory and can be
executed with a command :cli:`python sut/login.py`. Attempting to log
in with a non-existent user account or with an invalid password
results in the same error message::

    > python sut/login.py login nobody P4ssw0rd
    Access Denied

After creating a user account with valid password login succeeds::

    > python sut/login.py create fred P4ssw0rd
    SUCCESS

    > python sut/login.py login fred P4ssw0rd
    Logged In

There are two requirements that a password must fulfill to be valid: it must
be between 7-12 characters long, and it must contain lower and upper case
letters and numbers, but it must not contain special characters. Trying to
create a user with invalid password fails::

    > python sut/login.py create fred short
    Creating user failed: Password must be 7-12 characters long

    > python sut/login.py create fred invalid
    Creating user failed: Password must be a combination of lowercase and
    uppercase letters and numbers

Changing password with invalid credentials results in the same error message
as logging in with invalid credentials. The validity of new password is
verified and if not valid, an error message is given::

    > python sut/login.py change-password fred wrong NewP4ss
    Changing password failed: Access Denied

    > python sut/login.py change-password fred P4ssw0rd short
    Changing password failed: Password must be 7-12 characters long

    > python sut/login.py change-password fred P4ssw0rd NewP4ss
    SUCCESS

The application uses a simple database file to keep track on user
statuses. The file is located in operating system dependent temporary
directory.


Test cases
==========

First test cases
----------------

Robot Framework test cases are created using a simple tabular syntax. For example the following table has two tests:

   * User can create an account and log in
   * User cannot log in with bad password

.. table::
   :class: example

   =====================================  =================================  ==============  ==============
               Test Case                                Action                  Argument        Argument
   =====================================  =================================  ==============  ==============
   User can create an account and log in  Create Valid User                  fred            P4ssw0rd
   \                                      Attempt to Login with Credentials  fred            P4ssw0rd
   \                                      Status Should Be                   Logged In
   \
   User cannot log in with bad password   Create Valid User                  betty           P4ssw0rd
   \                                      Attempt to Login with Credentials  betty           wrong
   \                                      Status Should Be                   Access Denied
   =====================================  =================================  ==============  ==============

Notice that these tests read almost like manual tests written in
English rather than like automated test cases. Robot Framework uses the
keyword-driven approach that supports writing tests that capture the
essence of the actions and expectations in natural language. Test
cases are constructed from keywords (normally in the second column) and
their possible arguments.


Higher-level test cases
-----------------------

Test cases can also be created using only high-level keywords that
take no arguments. This style allows using totally free text which is
suitable for communication even with non-technical customers or
other stakeholders. Robot Framework does not enforce any particular
style for writing test cases, and it is possible to use for example
*given-when-then* format popularized by `behavior-driven development`__
(BDD) like in the example below.

__ http://en.wikipedia.org/wiki/Behavior_driven_development

.. table::
   :class: example

   ========================  ===========================================
           Test Case                           Steps
   ========================  ===========================================
   User can change password  Given a user has a valid account
   \                         when she changes her password
   \                         then she can log in with the new password
   \                         and she cannot use the old password anymore
   ========================  ===========================================

This kind of use-case or user-story-like test cases are ideally suited
for *acceptance test-driven development* (ATDD). In ATDD acceptance
tests are written before implementing actual product features and they
act also as requirements.


Data-driven test cases
----------------------

Quite often several test cases are otherwise similar but they have
slightly different input or output data. In these situations
*data-driven* test cases, like six tests below, allow varying the test
data without duplicating the workflow.

.. table::
   :class: example

   ==================================  ===============================================  =============  ======================
                Test Case                                                                 Password     Expected error message
   ==================================  ===============================================  =============  ======================
   Too short password                  Creating user with invalid password should fail  abCD5          ${PWD INVALID LENGTH}
   Too long password                   Creating user with invalid password should fail  abCD567890123  ${PWD INVALID LENGTH}
   Password without lowercase letters  Creating user with invalid password should fail  123DEFG        ${PWD INVALID CONTENT}
   Password without capital letters    Creating user with invalid password should fail  abcd56789      ${PWD INVALID CONTENT}
   Password without numbers            Creating user with invalid password should fail  AbCdEfGh       ${PWD INVALID CONTENT}
   Password with special characters    Creating user with invalid password should fail  abCD56+        ${PWD INVALID CONTENT}
   ==================================  ===============================================  =============  ======================

In these tests there is only one keyword per test case, and it is
responsible for trying to create a user with the provided password and
checking that creation fails with the expected error message. Because
only the first cell of the header row is processed, it is possible to
have meaningful column headers describing the data. Notice also that the
error messages are specified using variables_.


Keywords
========

Test cases are created from keywords that can come from three sources:
`built-in keywords`_ are always available, `library keywords`_ come
from imported test libraries, and so called `user keywords`_ can be
created using the same tabular syntax that is used for creating test
cases.


Built-in keywords
-----------------

Some generally useful keywords such as :name:`Get Time` and
:name:`Should Be Equal` are always available. Technically these
keywords come from a test library called BuiltIn_ and you can
see its documentation for a complete list of available keywords.


Library keywords
----------------

All lowest level keywords are defined in test libraries which are
implemented using standard programming languages. Robot Framework
comes with a `handful of libraries`__ including an OperatingSystem_
library to support common operating system functions, and a
Screenshot_ library for taking screenshots.  In addition to these
*standard libraries*, there are other libraries distributed in
separate open source projects, such as SeleniumLibrary_ for Web
testing. It is also easy to `implement your own libraries`__ when
there is no suitable library available.

__ http://code.google.com/p/robotframework/wiki/TestLibraries
__ `Creating test libraries`_

To be able to use keywords provided by a test library, it must be taken
into use.  Tests in this file need keywords from the standard
OperatingSystem library (e.g. :name:`Remove File`) as well as from a
custom made LoginLibrary (e.g. :name:`Attempt to login with
credentials`). Both of these libraries are imported in so called
*setting table* below.

.. table::
   :class: example

   ===============  ========================
       Setting                Value
   ===============  ========================
   Library          OperatingSystem
   Library          testlibs/LoginLibrary.py
   ===============  ========================


User-defined keywords
---------------------

One of the most powerful features of Robot Framework is the ability to
easily create new higher-level keywords from other keywords. The
syntax for creating these so called *user-defined keywords*, or *user
keywords* for short, is similar to the syntax that is used for
creating test cases. All the higher-level keywords needed in previous
test cases are created in the *keyword table* below.

.. table::
   :class: example

   ===============================================  =================================  ==============================  ================
                   Keyword                                         Action                          Argument                Argument
   ===============================================  =================================  ==============================  ================
   Clear login database                             Remove file                        ${DATABASE FILE}
   \
   Create valid user                                [Arguments]                        ${username}                     ${password}
   \                                                Create user                        ${username}                     ${password}
   \                                                Status should be                   SUCCESS
   \
   Creating user with invalid password should fail  [Arguments]                        ${password}                     ${error}
   \                                                Create user                        example                         ${password}
   \                                                Status should be                   Creating user failed: ${error}
   \
   Login                                            [Arguments]                        ${username}                     ${password}
   \                                                Attempt to login with credentials  ${username}                     ${password}
   \                                                Status should be                   Logged In
   \
   *# Used by BDD test cases (this is a comment)*
   Given a user has a valid account                 Create valid user                  ${USERNAME}                     ${PASSWORD}
   When she changes her password                    Change password                    ${USERNAME}                     ${PASSWORD}
   \                                                ...                                ${NEW PASSWORD}
   \                                                Status should be                   SUCCESS
   Then she can log in with the new password        Login                              ${USERNAME}                     ${NEW PASSWORD}
   And she cannot use the old password anymore      Attempt to login with credentials  ${USERNAME}                     ${PASSWORD}
   \                                                Status should be                   Access Denied
   ===============================================  =================================  ==============================  ================

User-defined keywords can include actions defined by other
user-defined keywords, built-in keywords, or library keywords.  As you
can see from this example, user-defined keywords can take parameters.
They can also return values and even contain FOR loops. For now, the
important thing to know is that user-defined keywords enable test
creators to create reusable steps for common action sequences.
User-defined keywords can also help the test author keep the tests as
readable as possible and use appropriate abstraction levels in
different situations.


Variables
=========

Defining Variables
------------------

Variables are an integral part of Robot Framework. Usually any data used in
tests that is subject to change is best defined as variables. Syntax for
variable definition is quite simple, as seen in this table:

.. table::
   :class: example

   ======================  =============================================================================
          Variable                                           Value
   ======================  =============================================================================
   ${USERNAME}             janedoe
   ${PASSWORD}             J4n3D0e
   ${NEW PASSWORD}         e0D3n4J
   \
   ${DATABASE FILE}        ${TEMPDIR}${/}robotframework-quickstart-db.txt
   \
   ${PWD INVALID LENGTH}   Password must be 7-12 characters long
   ${PWD INVALID CONTENT}  Password must be a combination of lowercase and uppercase letters and numbers
   ======================  =============================================================================

Variables can also be given from the command line which is useful if
the tests need to be executed in different environments. For example
this demo can be executed like::

   pybot --variable USERNAME:johndoe --variable PASSWORD:J0hnD0e quickstart.html

In addition to user defined variables, there are some built-in
variables that are always available. These variables include
:var:`${TEMPDIR}` and :var:`${/}` which are used in the above table.


Using variables
---------------

Variables can be used in most places in the test data. They are most
commonly used as arguments to keywords like the following test case
demonstrates.  Return values from keywords can also be assigned to
variables and used later. For example following :name:`Database Should
Contain` `user keyword`_ sets database content to :var:`${database}`
variable and then verifies the content using `built-in keyword`_
:name:`Should Contain`. Both library and user defined keywords can return
values.

.. table::
   :class: example

   =================================  =======================  ==============  ==============  ============
               Test Case                       Action             Argument        Argument       Argument
   =================================  =======================  ==============  ==============  ============
   User status is stored in database  [Tags]                   variables       database
   \                                  Create Valid User        ${USERNAME}     ${PASSWORD}
   \                                  Database Should Contain  ${USERNAME}     ${PASSWORD}     Inactive
   \                                  Login                    ${USERNAME}     ${PASSWORD}
   \                                  Database Should Contain  ${USERNAME}     ${PASSWORD}     Active
   =================================  =======================  ==============  ==============  ============

.. table::
   :class: example

   =======================  ================  ==============  =====================================  ============
           Keyword               Action          Argument                  Argument                    Argument
   =======================  ================  ==============  =====================================  ============
   Database Should Contain  [Arguments]       ${username}     ${password}                            ${status}
   \                        ${database} =     Get File        ${DATABASE FILE}
   \                        Should Contain    ${database}     ${username}\\t${password}\\t${status}
   =======================  ================  ==============  =====================================  ============


Organizing test cases
=====================

Test suites
-----------

Collections of test cases are called test suites in Robot
Framework. Every input file which contains test cases forms a test
suite. When `running this demo`_, you see test suite
:name:`Quickstart` in the console output. This name is got from the
file name and it is also visible in the report and log.

It is possible to organize test cases hierarchically by placing test
case files into directories and these directories into other
directories. All these directories automatically create higher level
test suites that get their names from directory names.  Since test
suites are just files and directories, they are trivially placed into
any version control system.

You can test running a directory as a test suite by running following
command in the directory where this guide is located::

   pybot .


Setup and teardown
------------------

If you want a set of actions to occur before and after each test
executes, use the :name:`Test Setup` and :name:`Test Teardown`
settings like so:

.. table::
   :class: example

   ===============  ========================
       Setting                Value
   ===============  ========================
   Test Setup       Clear Login Database
   Test Teardown
   ===============  ========================

Similarly you can use the :name:`Suite Setup` and :name:`Suite
Teardown` settings to specify actions to be executed before and after
an entire test suite executes.


Using tags
----------

Robot Framework allows setting tags for test cases to give them free
metadata.  Tags can be set for all test cases in a file with
:name:`Default Tags` or :name:`Force Tags` settings like in the table
below. It is also possible to define tags for single test case like in
earlier__ :name:`User status is stored in database` test.

__ `Using variables`_

.. table::
   :class: example

   ==============  ===========  ===========
       Setting        Value        Value
   ==============  ===========  ===========
   Force Tags      quickstart
   Default Tags    example      smoke
   ==============  ===========  ===========

When you look at a report after test execution, you can see that tests
have specified tags associated with them and there are also statistics
generated based on tags. Tags can also be used for many other
purposes, one of the most important being the possibility to select
what tests to execute. You can try for example following commands::

   pybot --include smoke quickstart.html
   pybot --exclude database quickstart.html


Creating test libraries
=======================

Robot Framework offers a simple API for creating test libraries, both with
Python and Java. The `user guide`_ contains detailed description with examples.

Below is the source code of :name:`LoginLibrary` test library used in
this guide. You can see, for example, how the keyword :name:`Create
User` is mapped to actual implementation of method
:code:`create_user`.

.. sourcecode:: python

   testlibs/LoginLibrary.py


.. footer:: Generated by reStructuredText_. Syntax highlighting by Pygments_.


.. Link targets:

.. _user keywords: `User-defined keywords`_
.. _user keyword: `user keywords`_
.. _built-in keyword: `Built-in keywords`_

.. _User Guide: http://code.google.com/p/robotframework/wiki/UserGuide
.. _Robot Framework User Guide: `User Guide`_
.. _installation instructions: http://code.google.com/p/robotframework/wiki/Installation
.. _download page: http://code.google.com/p/robotframework/downloads/list
.. _BuiltIn: http://code.google.com/p/robotframework/wiki/BuiltInLibrary
.. _OperatingSystem: http://code.google.com/p/robotframework/wiki/OperatingSystemLibrary
.. _Screenshot: http://code.google.com/p/robotframework/wiki/ScreenshotLibrary
.. _SeleniumLibrary: http://code.google.com/p/robotframework-seleniumlibrary
.. _Python: http://python.org
.. _Jython: http://jython.org
.. _Easy Install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/
