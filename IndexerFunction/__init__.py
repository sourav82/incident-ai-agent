import azure.functions as func
import logging
from datetime import datetime

from indexer.confluence_indexer import run_indexer


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().isoformat()

    if mytimer.past_due:
        logging.warning("The timer is past due!")

    logging.info(f"Indexer function started at {utc_timestamp}")

    try:
        run_indexer()
        logging.info("Indexer completed successfully")

    except Exception as e:
        logging.error(f"Indexer failed: {str(e)}")
        raise

    logging.info("Indexer function finished")