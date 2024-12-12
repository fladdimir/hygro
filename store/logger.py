import argparse
import logging


logging.basicConfig()

logger = logging.getLogger("store")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-log",
    "--loglevel",
    default="info",
    help="Provide logging level. Example --loglevel debug, default=info",
)
args = parser.parse_args()
print(f"loglevel: {args.loglevel}")
logger.setLevel(args.loglevel.upper())
