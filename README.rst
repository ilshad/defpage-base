================
defpage.com base
================

Deploy
======

Create virtual environment and deploy site within it::

  $ git clone git@spacta.com:defpage/base.git
  $ cd defpage_site
  $ virtualenv --no-site-packages --distribute .
  $ bin/pip install -e .

Run tests::

  $ bin/python setup.py test

Run site for development::

  $ bin/pserve development.ini --reload

Run site in production::

  $ bin/pserve production.ini --daemon
