========================
Hamlish-Jinja
========================

Overview
========

An extension for Jinja2 that adds support for HAML-like templates

Forked from `Pitmairen/hamlish-jinja <https://github.com/Pitmairen/hamlish-jinja>`_

Usage
=====

Install
--------

You can install the latest version with pip

::

    pip install git+https://codeberg.org/barkshark/hamlish

or

::

    pip install hamlish

Basic Usage
-----------

To use this extension you just need to add it to you jinja environment and use ".haml", ".jhaml", or
".jaml" as an extension for your templates.

.. code-block:: python

    from jinja2 import Environment
    from hamlish import HamlishExtension

    env = Environment(extensions = [HamlishExtension])
