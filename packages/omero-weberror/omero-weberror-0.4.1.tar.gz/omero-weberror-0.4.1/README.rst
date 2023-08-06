.. image:: https://github.com/ome/omero-weberror/workflows/OMERO/badge.svg
    :target: https://github.com/ome/omero-weberror/actions

.. image:: https://badge.fury.io/py/omero-weberror.svg
    :target: https://badge.fury.io/py/omero-weberror


OMERO.weberror
==============
OMERO.web app that helps testing errors, notification logic etc.

Requirements
------------

* OMERO.web 5.6 or newer.

Installing from PyPI
--------------------

This section assumes that an OMERO.web is already installed.

Install the app using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install omero-weberror

Add weberror custom app to your installed web apps:

::

    $ omero config append omero.web.apps '"omero_weberror"'

Now restart OMERO.web as normal.

Release process
---------------

This repository uses `bump2version <https://pypi.org/project/bump2version/>`_ to manage version numbers.
To tag a release run::

    $ bumpversion release

This will remove the ``.dev0`` suffix from the current version, commit, and tag the release.

To switch back to a development version run::

    $ bumpversion --no-tag [major|minor|patch]

specifying ``major``, ``minor`` or ``patch`` depending on whether the development branch will be a `major, minor or patch release <https://semver.org/>`_. This will also add the ``.dev0`` suffix.

Remember to ``git push`` all commits and tags.

License
-------

OMERO.weberror is released under the AGPL.

Copyright
---------

2016-2020, The Open Microscopy Environment
