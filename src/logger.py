
import logging

# TODO depois adicionar um CLI e passar verboso ou nao por la
logger = logging.getLogger(__name__)
verbose = True

logging.basicConfig(
    level=logging.DEBUG if verbose else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

