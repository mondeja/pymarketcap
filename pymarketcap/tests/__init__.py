# -*- coding: utf-8 -*-

"""Shared interfaces tests modules."""

from pymarketcap.errors import CoinmarketcapHTTPError

def type_test(map_types, key, value):
    """Test every type of the dictionary pairs
    key-values.

    Args:
        map_types (dict): Name of the keys and type
            or types that will be tested against it
            using ``isinstance(value, map_types[key])``
        key (str): Key that will be tested.
        value (str): Value name that will be tested.

    Raises:
       ``AssertionError`` if types and keys doesn't match.
    """
    try:
        assert isinstance(value, map_types[key])
    except AssertionError as err:
        print("Key: %s\nValue: %r\n" % (key, value))
        raise err

def assert_cryptocurrency_or_exchange_types(res):
    for key, value in res.items():
        if key == "id":
            assert isinstance(value, int)
        else:
            assert isinstance(value, str)

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
                except CoinmarketcapHTTPError:
                    sleep(THROTTLE)
                else:
                    error = False
                    ATTEMPTS -= 1
            return response
        return wrapper
    return real_decorator

def disabled_decorator(func):
    """This decorator disables the provided function, and does nothing."""
    def empty_func(*args,**kargs):
        pass
    return empty_func
