import argparse
import os
import logging
from la_ayudante.eat_app.eat_app import EatAppWorker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    worker = EatAppWorker()
    worker.process_reservation_finish_times()


if __name__ == "__main__":
    main()
