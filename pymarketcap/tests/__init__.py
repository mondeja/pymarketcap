#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Shared interfaces tests modules."""

def type_test(map_types, key, value):
    try:
        assert isinstance(value, map_types[key])
    except AssertionError as err:
        print("Key: %s\nValue: %r\n" % (key, value))
        raise err

def restart_if_http_error(res):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            ATTEMPTS = 10
            THROTTLE = 3  # Seconds between attempts
            error = True
            while error:
                try:
                    if ATTEMPTS > 0:
                        response = func()
                    else:
                        raise RuntimeError(
                            "Maximum number of attempts reached"
                        )
                except IndexError:
                    sleep(THROTTLE)
                else:
                    error = False
                    ATTEMPTS -= 1
            return response
        return wrapper
    return real_decorator
