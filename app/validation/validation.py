import logging
from flask import abort
from schema import (SchemaError, SchemaMissingKeyError, SchemaForbiddenKeyError,
                    SchemaWrongKeyError)

def validate(data, validation_schema):
    delNone = lambda x: [i for i in x if i is not None]

    try:
        valid_data = validation_schema.validate(data)

        if valid_data == {}:
            abort(422, "No valid data")
        return valid_data

    except SchemaMissingKeyError as e:
        #for err in e.errors:
            #logging.getLogger(__name__).debug('Error: {}'.format(err))
        #for err in e.autos:
            #logging.getLogger(__name__).debug('Autos: {}'.format(err))
        abort(400, '\n'.join(delNone(e.autos)))

    except SchemaForbiddenKeyError as e:
        #for err in e.errors:
            #logging.getLogger(__name__).debug('Error: {}'.format(err))
        #for err in e.autos:
            #logging.getLogger(__name__).debug('Autos: {}'.format(err))
        abort(400, '\n'.join(delNone(e.errors)))

    except SchemaWrongKeyError as e:
        #for err in e.errors:
            #logging.getLogger(__name__).debug('Error: {}'.format(err))
        #for err in e.autos:
            #logging.getLogger(__name__).debug('Autos: {}'.format(err))
        abort(400, '\n'.join(delNone(e.errors)))

    except SchemaError as e:
        #for err in e.errors:
            #logging.getLogger(__name__).debug('Error: {}'.format(err))
        #for err in e.autos:
            #logging.getLogger(__name__).debug('Autos: {}'.format(err))
        abort(422, '\n'.join(delNone(e.errors)))
