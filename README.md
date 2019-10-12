# Faketime

Faketime is a thin python wrapper around the amazing C library [libfaketime](https://github.com/wolfcw/libfaketime), written
by [Wolfgang Hommel](https://github.com/wolfcw) which you can use to lie to UNIX processes about what time and date it is.


## Why does this wrapper exist?

* It provides an interface that is convenient and pythonic that you can use to lie to subprocesses run with python.
* It provides an python interface that is identical on both Mac OS X and Linux (libfaketime is used in a slightly different way on both).
* It provides a self contained library that can be installed in a virtualenv that runs consistently in any environment - installing libfaketime from package manager can instead get you older, buggy versions on different operating systems and package managers.

## Install

```
pip install faketime
```

## Using

```
>>> from commandlib import Command
>>> from faketime import Faketime
>>> from datetime import datetime
>>> faketime = Faketime("currenttime.txt")
>>> datecmd
{'LD_PRELOAD': '/full/path/to/virtualenv/site-packages/faketime/libfaketime.so.1', 'FAKETIME_TIMESTAMP_FILE': '/full/path/to/currenttime.txt'}


>>> datecmd = Command("date").with_env(**faketime.env_vars)
>>> datecmd.run()
[ should print current time ]

>>> faketime.change_time(datetime(2050, 6, 7, 10, 9, 22, 713689))
>>> datecmd.run()
Tue  7 Jun 10:09:21 BST 2050
```

This above example shows how to use faketime with [commandlib](https://hitchdev.com/commandlib/), although
the environment variables in the dict can be used with any command runner (e.g. Popen).

## What's the story behind this library?

This library can be used for a number of purposes, but I mainly built it so that I could write
tests with [hitchstory](https://hitchdev.com/hitchstory) that would lie to postgres,
django and celery simultaneously about what date and time it was.

Initially I tried using [freezegun](https://github.com/spulec/freezegun) to test the python code, but I realized that it only really
worked on one snippet of code at a time. Moreover:

* If that code executed a python process that contained other code that other code would get the *current* time, not the frozen time, breaking the test.
* It was simply incapable of faking, say, postgres's time, so if an SQL query embedded a datetime query then that would break the test.
