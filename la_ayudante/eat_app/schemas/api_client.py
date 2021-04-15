# Handle schemas for all objects that can be sent or received by the API.
# While possibly YAGNI, this allows automated introspection into the data
# structures returned by the API. By using strict serialization and validation,
# we can detect any changes in the API, emit an alert, and then possibly try to
# continue to process whatever work needs to be done.
from marshmallow import Schema, fields, validate


class RestaurantSchema(Schema):
    """ Schema for validating response when getting restaurant ID after
    authentication
    """
    id = fields.UUID(
        required=True
    )
    type = fields.String(
        required=True,
        validate=validate.OneOf([
            "restaurant",
        ])
    )
    # NOTE: attributes here is *HUGE* and I probably don't need it
    attributes = fields.Dict()
    # NOTE: relationships may be useful if/when multiple venues are being used
    relationships = fields.Dict()


class RestaurantUserPermissionSchema(Schema):
    id = fields.UUID(
        required=True
    )
    name = fields.String(
        required=True
    )
    description = fields.String(
        required=True
    )
    field_type = fields.Boolean(
        required=True
    )
    field_options = fields.List(
        # NOTE: May not be string
        fields.String(
            required=False
        ),
        required=True,
        allow_none=True
    )
    default = fields.Boolean(
        required=True
    )
    context = fields.List(
        fields.String(
            required=True
        ),
        required=True
    )
    group = fields.String(
        required=True
    )
    access_level = fields.String(
        required=True,
        validate=validate.OneOf([
            "customer",
        ])
    )
    error_message = fields.String(
        required=True
    )
    value = fields.Boolean(
        required=True
    )
    assigned = fields.Boolean(
        required=True
    )


class RestaurantUserAttributesSchema(Schema):
    """ Used to validate the attributes of a restaurant user when retrieving
    the restaurant ID 
    """
    # NOTE: the attributes are slightly different when authenticating vs.
    # a restaurant_user some relationships entity. The differences in these 
    # schemas is represented by separating the fields by commonality, then 
    # exclusivity.
    
    # Common fields (make required)
    name = fields.String(
        required=True
    )
    email = fields.Email(
        required=True
    )
    role = fields.String(
        required=True,
        # NOTE: expect different user roles in the future
        validate=validate.OneOf([
            "manager",
        ],
        error="User with role other than manager detected. Please update schema."
        )
    )
    # NOTE: May not be string
    color = fields.String(
        required=True,
        allow_none=True
    )
    taker = fields.Boolean(
        required=True
    )
    login = fields.Boolean(
        required=True
    )
    show_shared_guests = fields.Boolean(
        required=True
    )
    merge_guests = fields.Boolean(
        required=True
    )
    # NOTE: this might be Dict OR List
    permissions = fields.Dict(
        fields.Nested(
            RestaurantUserPermissionSchema,
            required=False
        ),
        required=False
    )

    # Authentication Only
    terms_and_conditions_accepted = fields.Boolean(
        required=False
    )
    marketing_accepted = fields.Boolean(
        required=False
    )
    token = fields.String(
        required=False
    )
    
    # TODO: WHERE ELSE AM I GETTING A USER FROM?
    # NOTE: May note be integer
    pin_code = fields.Integer(
        required=False,
        allow_none=True
    )
    server = fields.Boolean(
        required=False
    )
    last_sign_in = fields.DateTime(
        required=False
    )


class RestaurantUserSchema(Schema):
    """ Used to validate the response when getting the restaurant ID
    """
    id = fields.UUID(
        required=True
    )
    type = fields.String(
        required=True,
        validate=validate.OneOf([
            "restaurant_user",
        ]),
    )
    attributes = fields.Nested(
        RestaurantUserAttributesSchema,
        required=True
    )


class ReservationAttributesSchema(Schema):
    covers = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )
    created_by = fields.UUID(
        required=True,
        allow_none=True,
    )
    duration = fields.Integer(
        required=True
    )
    key = fields.String(
        required=True
    )
    notes = fields.String(
        required=True,
        allow_none=True
    )
    status = fields.String(
        required=True,
        validate=validate.OneOf([
            "confirmed",
            "not_confirmed",
            # it's not cancelled :(
            "canceled",
            "seated",
            "finished",
            ])
    )
    walk_in = fields.Boolean(
        required=True
    )
    # Unsure if this is the correct type
    wait_list_status = fields.String(
        required=True,
        allow_none=True
    )
    wait_list_table_ready_sms = fields.Boolean(
        required=True,
        allow_none=True
    )
    wait_list_duration = fields.Integer(
        required=True,
        default=0
    )
    # TODO: enumerate possible lock_statuses
    lock_status = fields.String(
        required=True,
        validate=validate.OneOf(
            "open",
        )
    )
    arrived_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    canceled_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    check_dropped_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    confirmed_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    created_at = fields.DateTime(
        required=True
    )
    denied_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    finished_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    no_show_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    seated_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    start_time = fields.DateTime(
        required=True
    )
    updated_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    wait_list_queued_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    wait_list_table_ready_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    wait_list_confirmed_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    wait_list_canceled_at = fields.DateTime(
        required=True,
        allow_none=True
    )
    online = fields.Boolean(
        required=True
    )
    comments = fields.List(
            fields.String(
                required=False
            ),
            required=True
        )
    # TODO: unsure what this actually does. It is a generic Object{} in the 
    # web app
    review = fields.Dict(
            required=True,
            allow_none=True
    )
    custom_tags = fields.List(
        fields.String(
            required=True,
            allow_none=True
        ),
        required=True
    )
    tags = fields.List(
        fields.String(
            required=True,
            allow_none=True
        ),
        required=True
    )


class ReservationSchema(Schema):
    id = fields.UUID(
        required=True
    )
    attributes = fields.Nested(
        ReservationAttributesSchema,
        required=True
    )
    type = fields.String(
        required=True,
        default="reservation"
    )
    relationships = fields.Dict(
        required=True,


    )

    # how to handle relationships?
    # handle as plain dict -> how to handle nested lists?
    # handle as nested schemas -> super fucking overkill
class ReservationsSchema(Schema):
    pass

class TableAttributes(Schema):
    """
    """
    # TODO: find out how to validate against other fields
    max_covers = fields.Int(
        required=True,
        #validate=validate.Range(min=min_covers)
    )
    min_covers = fields.Int(
        required=True,
        #validate=validate.Range(min=0, max=max_covers)
    )
    number = fields.String(required=True)
    pos_service_table_id = fields.UUID(
        required=False,
        allow_none=True
    )
    restaurant_server_id = fields.UUID(
        required=False,
        allow_none=True
    )
    room_id = fields.UUID(
        required=False
    )
    rotation = fields.Integer(
        required=True
    )
    shape = fields.String(
        required=True
    )
    size = fields.String(
        required=True,
        validate=validate.Regexp(r"^\d+x\d+$")
    )
    sold_online = fields.Boolean(
        required=True
    )
    updated_at = fields.DateTime(
        required=True
    )
    # TODO: check if these are always 0>n>1
    x = fields.Float(
        required=True
    )
    y = fields.Float(
        requird=True
    )

class TableSchema(Schema):
    id = fields.UUID(
        required=True
    )
    type = fields.String(
        required=True,
        default='table'
    )
    attributes = fields.Nested(TableAttributes)

class TablesSchema(Schema):
    tables = fields.List(
        fields.Nested(TableSchema)
    )
