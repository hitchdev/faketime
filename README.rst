Faketime
========

Libfaketime is a C library which can fake the passage of time for UNIX applications, written
by Wolfgang Hommel.

This library compiles it and gives some python convenience functions to run it, abstracting
away the differences between running it under Linux and Mac OS X.

Get extra environment vars you need to run your process with::

    >>> import faketime
    >>> faketime.environment_vars("filename.txt")

Write a new time to file::

    >>> import datetime
    >>> faketime.change_time("filename.txt", datetime.datetime(2050, 6, 7, 10, 9, 22, 713689))
    >>> import flyingcar

As soon as you have written the time to file, the new process should have picked up the
new time.
