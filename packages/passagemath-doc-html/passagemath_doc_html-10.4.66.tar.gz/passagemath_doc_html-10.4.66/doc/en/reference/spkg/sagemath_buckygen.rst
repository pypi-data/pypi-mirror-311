.. _spkg_sagemath_buckygen:

=========================================================================================
sagemath_buckygen: Generation of nonisomorphic fullerenes with buckygen
=========================================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2024 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (Windows Subsystem for Linux).

See https://doc.sagemath.org/html/en/installation/index.html
for general installation instructions.


About this pip-installable distribution package
-----------------------------------------------

This pip-installable distribution ``passagemath-buckygen`` provides an interface
to `buckygen <http://caagt.ugent.be/buckygen/>`_, a program for the efficient
generation of all nonisomorphic fullerenes.


What is included
----------------

* Binary wheels on PyPI contain prebuilt copies of buckygen.


Examples
--------

Using buckygen programs on the command line::

    $ pipx run --pip-args="--prefer-binary" --spec "passagemath-buckygen" sage -sh -c buckygen

Finding the installation location of an buckygen program::

    $ pipx run --pip-args="--prefer-binary" --spec "passagemath-buckygen[test]" ipython

Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_buckygen`
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_sage_conf`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_environment`

Version Information
-------------------

package-version.txt::

    10.4.66

version_requirements.txt::

    passagemath-buckygen ~= 10.4.66.0


Equivalent System Packages
--------------------------

(none known)

