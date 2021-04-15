import logging

log = logging.getLogger(__name__)

def conforms_to_schema(model, schema):
    """ Tests some object against a schema and handles appropriate logging. """
    validation_errors = schema.validate(model)
    if validation_errors != {}:
        return False
    else:
        return True
