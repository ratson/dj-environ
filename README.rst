==========
Dj-environ
==========

Dj-environ allows you to utilize 12factor inspired environment variables to configure your Django application.

|pypi| |downloads| |license|


This is your `settings.py` file before you have installed **dj-environ**

.. code-block:: python

    import os
    SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'githubbedpassword',
            'HOST': '127.0.0.1',
            'PORT': '8458',
        }
        'extra': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'database.sqlite')
        }
    }

    MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
    MEDIA_URL = 'media/'
    STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
    STATIC_URL = 'static/'

    SECRET_KEY = '...im incredibly still here...'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '127.0.0.1:11211', '127.0.0.1:11212', '127.0.0.1:11213',
            ]
        },
        'redis': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379:1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': 'redis-githubbed-password',
            }
        }
    }

After:

.. code-block:: python

    import environ
    root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
    env = environ.Env(DEBUG=(bool, False),) # set default values and casting
    environ.Env.read_env() # reading .env file

    SITE_ROOT = root()

    DEBUG = env('DEBUG') # False if not in os.environ
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
    }

    public_root = root.path('public/')

    MEDIA_ROOT = public_root('media')
    MEDIA_URL = 'media/'
    STATIC_ROOT = public_root('static')
    STATIC_URL = 'static/'

    SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

    CACHES = {
        'default': env.cache(),
        'redis': env.cache('REDIS_URL')
    }

You can also pass ``read_env()`` an explicit path to the ``.env`` file.

Create a ``.env`` file:

.. code-block:: bash

    DEBUG=on
    # DJANGO_SETTINGS_MODULE=myapp.settings.dev
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
    # SQLITE_URL=sqlite:///my-local-sqlite.db
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379:1?client_class=django_redis.client.DefaultClient&password=redis-un-githubbed-password


How to install
==============

::

    $ pip install dj-environ


How to use
==========

There are only two classes, ``environ.Env`` and ``environ.Path``

.. code-block:: python

    >>> import environ
    >>> env = environ.Env(
            DEBUG=(bool, False),
        )
    >>> env('DEBUG')
    False
    >>> env('DEBUG', default=True)
    True

    >>> open('.myenv', 'a').write('DEBUG=on')
    >>> environ.Env.read_env('.myenv') # or env.read_env('.myenv')
    >>> env('DEBUG')
    True

    >>> open('.myenv', 'a').write('\nINT_VAR=1010')
    >>> env.int('INT_VAR'), env.str('INT_VAR')
    1010, '1010'

    >>> open('.myenv', 'a').write('\nDATABASE_URL=sqlite:///my-local-sqlite.db')
    >>> env.read_env('.myenv')
    >>> env.db()
    {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'my-local-sqlite.db', 'HOST': '', 'USER': '', 'PASSWORD': '', 'PORT': ''}

    >>> root = env.path('/home/myproject/')
    >>> root('static')
    '/home/myproject/static'


Supported Types
===============

- str
- bool
- int
- float
- json
- list (FOO=a,b,c)
- tuple (FOO=(a,b,c))
- dict (BAR=key=val,foo=bar) #environ.Env(BAR=(dict, {}))
- dict (BAR=key=val;foo=1.1;baz=True) #environ.Env(BAR=(dict(value=unicode, cast=dict(foo=float,baz=bool)), {}))
- url
- path (environ.Path)
- db_url
    -  PostgreSQL: postgres://, pgsql://, psql:// or postgresql://
    -  PostGIS: postgis://
    -  MySQL: mysql:// or mysql2://
    -  MySQL for GeoDjango: mysqlgis://
    -  SQLITE: sqlite://
    -  SQLITE with SPATIALITE for GeoDjango: spatialite://
    -  Oracle: oracle://
    -  LDAP: ldap://
- cache_url
    -  Database: dbcache://
    -  Dummy: dummycache://
    -  File: filecache://
    -  Memory: locmemcache://
    -  Memcached: memcache://
    -  Python memory: pymemcache://
    -  Redis: rediscache://
- search_url
    - ElasticSearch: elasticsearch://
    - Solr: solr://
    - Whoosh: whoosh://
    - Xapian: xapian://
    - Simple cache: simple://
- email_url
    - SMTP: smtp://
    - SMTP+SSL: smtp+ssl://
    - SMTP+TLS: smtp+tls://
    - Console mail: consolemail://
    - File mail: filemail://
    - LocMem mail: memorymail://
    - Dummy mail: dummymail://

Tips
====

Using unsafe characters in URLs
-------------------------------

In order to use unsafe characters you have to encode with ``urllib.parse.encode`` before you set into ``.env`` file.

.. code-block::

    DATABASE_URL=mysql://user:%23password@127.0.0.1:3306/dbname


See https://perishablepress.com/stop-using-unsafe-characters-in-urls/ for reference.

Email settings
--------------

In order to set email configuration for django you can use this code:

.. code-block:: python

    EMAIL_CONFIG = env.email_url(
        'EMAIL_URL', default='smtp://user@:password@localhost:25')

    vars().update(EMAIL_CONFIG)


Tests
=====

::

    $ git clone https://github.com/ratson/dj-environ.git
    $ cd dj-environ/
    $ python setup.py test


Credits
=======

This is a fork of `django-environ <https://github.com/joke2k/django-environ>`_,
which has the following differences,

* Support PostgreSQL URL using unix domain socket paths, e.g. postgres:////var/run/postgresql/db


.. |pypi| image:: https://img.shields.io/pypi/v/dj-environ.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/dj-environ
    :alt: Latest version released on PyPi

.. |downloads| image:: https://img.shields.io/pypi/dm/dj-environ.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dj-environ
    :alt: Monthly downloads

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/ratson/dj-environ/master/LICENSE.txt
    :alt: Package license
