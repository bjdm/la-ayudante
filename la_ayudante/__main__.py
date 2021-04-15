import argparse
import logging
import os
import sys

from la_ayudante.eat_app import EatAppWorker


log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help="verbose output")
    parser.add_argument('-u', '--eat_app_username', type=str, help="Eat App login email")
    parser.add_argument('-p', '--eat_app_password', type=str, help="Eat App password")
    # Implement variable logging level
    #parser.add_argument('--log_level', help="Set logging level")

    args = parser.parse_args()
    if args.eat_app_username is None:
        try:
            args.eat_app_username = os.environ['EAT_APP_USERNAME']
        except KeyError:
            log.error("No Eat App username supplied or found in environment")
            sys.exit(1)
    if args.eat_app_password is None:
        try:
            args.eat_app_username = os.environ['EAT_APP_PASSWORD']
        except KeyError:
            log.error("No Eat App password supplied or found in environment")
            sys.exit(1)

    eat_app_worker = EatAppWorker(username=args.eat_app_username, password=args.eat_app_password)
    eat_app_worker.process_reservation_finish_times()


if __name__ == "__main__":
    main()
