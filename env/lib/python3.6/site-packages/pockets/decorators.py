# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A pocket full of useful decorators!"""


__all__ = ['classproperty']


def classproperty(cls):
    """
    Decorator to create a read-only class property similar to classmethod.

    For whatever reason, the @property decorator isn't smart enough to
    recognize @classmethods and behaves differently on them than on instance
    methods.  This decorator may be used like to create a class-level property,
    useful for singletons and other one-per-class properties.

    Note:
        Class properties created by @classproperty are read-only. Any attempts
        to write to the property will erase the @classproperty, and the
        behavior of the underlying method will be lost.

    >>> class MyClass(object):
    ...     @classproperty
    ...     def myproperty(cls):
    ...         return '{0}.myproperty'.format(cls.__name__)
    >>> MyClass.myproperty
    'MyClass.myproperty'

    """
    class _classproperty(property):
        def __get__(self, cls, owner):
            return self.fget.__get__(None, owner)()

        def getter(self, fget):
            raise AttributeError('@classproperty.getter is not supported')

        def setter(self, fset):
            raise AttributeError('@classproperty.setter is not supported')

        def deleter(self, fdel):
            raise AttributeError('@classproperty.deleter is not supported')
    return _classproperty(classmethod(cls))
