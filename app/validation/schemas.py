from schema import (Schema, Use, And, Optional, Hook,
                    SchemaForbiddenKeyError, Regex)
from datetime import date, time, datetime


class Forbidden(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(Forbidden, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError(
            'Forbidden key encountered: {} in {}'.format(nkey, data),
            self._error
        )


class unknownKey(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(unknownKey, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError(
            'Unknown key encountered: {} in {}'.format(nkey, data),
            '{}: {}'.format(self._error, nkey)
        )


login = Schema(
    {
        'email': Use(str),
        'password': Use(str),
        Optional('next'): Use(str),
    },
    ignore_extra_keys=True
)

register = Schema(
    {
        'email': Use(str),
        'password': Use(str),
        'name': Use(str),
        'surname': Use(str)
    },
    ignore_extra_keys=True
)

change_password = Schema(
    {
        'old_password': Use(str),
        'new_password': Use(str)
    },
    ignore_extra_keys=True
)

password = Schema(
    {
        'password': Use(str)
    },
    ignore_extra_keys=True
)

reset_password = Schema(
    {
        'email': Use(str)
    },
    ignore_extra_keys=True
)
