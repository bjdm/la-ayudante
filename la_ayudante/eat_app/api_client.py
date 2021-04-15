import requests
import logging
from datetime import date, datetime

from la_ayudante.eat_app.schemas.api_client import (
    RestaurantSchema,
    RestaurantUserSchema,
    TableSchema,
    ReservationSchema
)
log = logging.getLogger(__name__)


# TODO: change to requests-oauthlib or implement AuthBase subclass
# TODO: add decorator (or see if I can do it with requests hooks) for
#       rate limiting
# TODO: implement a HTTPAdapter to handle retries and connection resets
class ApiClient:
    """
    An object to wrap any http requests in a session to transparently handle
    authentication and cookie management.
    """
    def __init__(self, base_url, username=None, password=None,
                 restaurant_id=None, token=None):
        # TODO: remove
        self.base_url = base_url
        self.user_name = username
        self.password = password
        self.restaurant_id = None
        self.session = requests.Session()
        self.session.verify = True
        self.token = token
        self.headers = {}

        if self.token is None or self.restaurant_id is None or \
                self.headers == {}:
            self._set_headers()


    def update_note(self, id, note):
        response = self.session.put(self.base_url + 'reservations/' + str(id), data={'notes': note })
        if response.status_code == 200:
            log.info("Successfully updated reservation {}".format(id))
        else:
            log.debug(note)
            log.warn("Unable to update reservation {}".format(id))


    def get_tables_from_api(self, uri='tables', limit=100):
        url = self.base_url + uri + '?limit=' + str(limit)
        log.debug("Requesting list of tables from API")
        response = self.session.get(url)

        if response.status_code == 200:
            log.debug("Response 200")
            # Response was good. Check data
            tables_json = response.json()['data']
            if len(tables_json) == 0:
                log.error("HTTP request to get tables from API was successful, \
                        but no tables were returned")
                # TODO: fix this error raising
                raise Exception
            if len(tables_json) >= limit:
                log.warn("Number of tables equal to limit. Please check all \
                        tables were successfully loaded.")
            log.info("Retrieved {} tables from API".format(len(tables_json)))
            #return tables_json
            # TODO: remove
            return validate_tables(tables_json)
            
        else:
            log.error("Request to get tables from API failed")
            # TODO: use cached tables if availabe
            raise Exception

    def get_reservations_from_api(
        self,
        uri='reservations',
        limit=1000,
        date=date.today().strftime("%Y%m%d")
    ):
        url = self.base_url + uri + '?start_time_on=' + date + '&limit=' + str(limit)
        log.debug("Requesting list of tables from API")
        response = self.session.get(url)

        if response.status_code == 200:
            log.debug("Response 200")
            # Response was good. Check data
            reservations_json = response.json()['data']
            if len(reservations_json) == 0:
                log.error("HTTP request to get reservations from API was \
                        successful, but no reservations were returned")
                # TODO: fix this error raising
                raise Exception
            if len(reservations_json) >= limit:
                log.warn("Number of reservations equal to limit. Please check all \
                        reservations were successfully loaded.")
            log.info("Retrieved {} reservations from API".format(len(reservations_json)))
            #return reservations_json
            # TODO: remove
            return validate_reservations(reservations_json)
            
        else:
            log.error("Request to get reservations from API failed")
            # TODO: use cached tables if availabe
            raise Exception



    def get_tables(self, uri, limit=100):
        """
        Gets the list of tables in the restaurant
        params:
            uri: (str) the resource identifier of the api to get the tables
            limit: (int) limit the number of tables when retrieving from the
            API. The webapp uses a limit of 100000. Using 100 here to leave
            some room for error.
        """
        url = self.base_url + str(uri) + '?limit=' + str(limit)
        log.info("Getting tables.")
        response = self.session.get(url)

        if response.status_code == 200:
            # we got back more tables than our limit. something's probably gone
            # terribly wrong
            tables = response.json()['data']
            if len(tables) >= limit:
                log.info("Retrieved {} tables.".format(len(tables)))
            return {t['id']: t['attributes']['number'] for t in tables}
        else:
            log.error("Failed to retrieve list of tables. HTTP {}".format(
                response.status_code)
            )
            raise Exception

    def get_reservations(self, uri, limit=1000, date=date.today().strftime("%Y%m%d")):
        """
        Returns a list of reservation dictionaries.
        """
        # TODO: Remove
        url = self.base_url + uri + '?start_time_on=' + date + '&limit=' + str(limit)
        log.info("Getting list of reservations for {}".format(date))
        response = self.session.get(url)

        if response.status_code == 200:
            reservations = response.json()['data']
            if len(reservations) >= limit:
                log.warn("Retrieved the maximum amount of reservations. Please\
                         check all tables have been successfully updated on \
                        completion.")
            log.info("Retrieved {} reservations".format(len(reservations)))
            return reservations
        else:
            log.error("Unable to retrieve reservations:\n{}\n{}\n{}".format(
                response.status_code,
                response.headers,
                response.text
                )
            )


    def _set_headers(self):
        """
        Authenticate with the api then set the required headers (restaurant id)
        """
        log.info("Attempting to set EatApp session headers")
        if self.token is None:
            self.token = self._get_authorization_token()
        self.session.headers["Authorization"] = 'Bearer ' + str(self.token)

        if self.restaurant_id is None:
            self.restaurant_id = self._get_restaurant_id()
        self.session.headers["X-Restaurant-ID"] = self.restaurant_id


    def _get_restaurant_id(self):
        # Get the restaurant id for the header
        # Use the request params the web app does
        # TODO: do I need to test for authorization failure here?
        log.info("Getting restaurant id for user: {}".format(self.user_name))
        response = self.session.get(
                self.base_url + 'restaurants?sort=name:asc&limit=100'
            )
        if response.status_code == 200:
            if len(response.json()['data']) > 1:
                log.error("Cannot unambiguously determine restaurant: more than \
                        one({}) restaurant ID returned.".format(
                            len(response.json()['data'])
                        )
                    )
            elif len(response.json()['data']) == 1:
                if valid_schema(RestaurantSchema(), response.json()['data'][0]):
                    restaurant_id = response.json()['data'][0]['id']
                    log.info("Got restaurant id for {}: {}".format(
                        self.user_name,
                        restaurant_id
                        )
                    )
                    return restaurant_id
                else:
                    # TODO: add option to continue anyway
                    log.info("Continuing after failed schema validation when \
                            getting restaurant ID")
                    return restaurant_id
            else:
                log.error("Failed to get restaurant id for {}".format(self.user_name))
        else:
            log.error("Failed to GET restaurant IDs(Code: {}".format(
                response.status_code
            )
        )


    def _get_authorization_token(self):
        """
        Authenticates with the server and returns the authorization token.
        TODO: decide whether to pull in config here or elsewhere (NB: probs
                elsewhere.
        """
        log.info("Attempting to authenticate as {}".format(self.user_name))
        # Authenticate and get authorization token
        data = {
            'email': self.user_name,
            'password': self.password,
        }
        response = self.session.post(
                        self.base_url + 'authentication',
                        json=data
                    )
        if response.status_code == 200:
            log.info("Successfully authenticated as {}".format(self.user_name))
            if valid_schema(RestaurantUserSchema(), response.json()['data']):
                log.debug("Successfully validated RestaurantUserSchema")
            else:
                log.info("Continuing after failed schema validation when \
                        getting authorization token")
            return response.json()['data']['attributes']['token']
        else:
            log.error("Authentication for {} failed".format(self.user_name))


def valid_schema(schema, model):
    """ Tests some object against a schema and handles appropriate logging. """
    validation_errors = schema.validate(model)
    if validation_errors != {}:
        log.warn("Validation errors:\n{}".format(validation_errors))
        return False
    else:
        return True


def validate_reservations(raw_reservations):
    reservations = []
    for raw_reservation in raw_reservations:
        if valid_schema(ReservationSchema(), raw_reservation):
            log.debug("Reservation ({}) successfully validated".format(raw_reservation['id']))
            reservations.append(ReservationSchema().load(raw_reservation))
        else:
            log.warn("A reservation ({}) failed schema validation".format(raw_reservation['id']))
    if len(reservations) == 0:
        log.error("No reservations were successfully serialised. Exiting")
        return None
    elif len(reservations) < len(raw_reservations):
        log.warn("Some reservations were not successfully validated")
    elif len(reservations) == len(raw_reservations):
        log.info("All reservations({}) successfully validated".format(len(reservations)))
    else:
        log.warn("Validated more reservations than API returned. This should not \
                happen")
        return None
    return reservations

def validate_tables(raw_tables):
    """ Gets the tables from the server, validates their schema, and
    returns a list of serialised tables
    """
    tables = []
    for raw_table in raw_tables:
        if valid_schema(TableSchema(), raw_table):
            log.debug("Table {}({}) successfully validated".format(
                raw_table['attributes']['number'],
                raw_table['id']))
            tables.append(TableSchema().load(raw_table))
        else:
            log.warn("A table ({}) failed schema validation".format(raw_table['id']))
    if len(tables) == 0:
        log.error("No tables were successfully serialised. Exiting")
        return None
    elif len(tables) < len(raw_tables):
        log.warn("Some tables were not successfully validated")
    elif len(tables) == len(raw_tables):
        log.info("All tables({}) successfully validated".format(len(tables)))
    else:
        log.warn("Validated more tables than API returned. This should not \
                happen")
        return None
    return tables
