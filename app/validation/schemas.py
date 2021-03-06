from schema import (Schema, Use, And, Optional, Hook,
                    SchemaForbiddenKeyError, Regex)
from datetime import date, time, datetime


class Forbidden(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(Forbidden, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError(
            f'Forbidden key encountered: {nkey} in {data}',
            self._error
        )


class unknownKey(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(unknownKey, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError(
            f'Unknown key encountered: {nkey} in {data}',
            f'{self._error}: {nkey}'
        )


login = Schema(
    {
        'email': Use(str.lower),
        'password': Use(str),
        Optional('next'): Use(str),
    },
    ignore_extra_keys=True
)

register = Schema(
    {
        'email': Use(str.lower),
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

email = Schema(
    {
        'email': Use(str.lower)
    },
    ignore_extra_keys=True
)

add_machine = Schema(
    {
        'domain': Use(str),
        'address': Use(str),
    },
    ignore_extra_keys=True
)

address = Schema(
    {
        'address': Use(str),
    },
    ignore_extra_keys=True
)

manage_access = Schema(
    {
        'email': Use(str),
        'address': Use(str),
    },
    ignore_extra_keys=True
)

add_key = Schema(
    {
        'name': Use(str),
        'key': Use(str),
    },
    ignore_extra_keys=True
)

remove_key = Schema(
    {
        'u_email': Use(str.lower),
        'k_id': Use(int),
    },
    ignore_extra_keys=True
)

superadmin_reset_password = Schema(
    {
        'token': Use(str),
        'new_password': Use(str)
    },
    ignore_extra_keys=True
)