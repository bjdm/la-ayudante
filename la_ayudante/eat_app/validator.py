import logging

from la_ayudante.eat_app.schemas.api_client import TableSchema, ReservationSchema

log = logging.getLogger(__name__)


class Validator:
    def __init__(self, schema):
        self.schema = schema

    def is_valid_model(self, model):
        validation_errors = self.schema.validate(model)
        if validation_errors != {}:
            log.warn("Validation errors:\n{}".format(validation_errors))
            return False
        else:
            return True

    def get_valid_items(self, data):
        items = []
        for datum in data:
            if datum.is_valid_model():
                # TODO: find a way to log this effectively
                log.debug("Validated model.")
                items.append(self.schema.load(datum))
            else:
                log.warn("Model failed schema validation.")
        
        if len(items) == 0:
            log.error("No objects were successfully serialised. Exiting...")
            exit(1)
        elif len(items) < len(data):
            log.warn("{} items failed validation.".format(
                len(data) - len(items)
                )
            )

        elif len(items) == len(data):
            log.info("Successfully validated all {} items.".format(
                len(items)
                )
            )
        else:
            log.error("Validated more items than received. Shouldn't happen.")
            exit(1)

        return items


class TableValidator(Validator):
    def __init__(self):
        self.schema = TableSchema()


class ReservationValidator(Validator):
    def __init__(self):
        self.schema = ReservationSchema()
