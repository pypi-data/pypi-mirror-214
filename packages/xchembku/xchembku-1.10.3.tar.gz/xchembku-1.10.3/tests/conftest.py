import logging
import os
import shutil

import pytest

# Formatting of testing log messages.
from dls_logformatter.dls_logformatter import DlsLogformatter

# Version of the package.
# from xchembku_lib.version import meta as version_meta

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def constants(request):

    constants = {}

    yield constants


# --------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def logging_setup():
    # print("")

    formatter = DlsLogformatter(type="long")
    logger = logging.StreamHandler()
    logger.setFormatter(formatter)
    logging.getLogger().addHandler(logger)

    # Log level for all modules.
    logging.getLogger().setLevel("DEBUG")

    # Turn off noisy debug.
    logging.getLogger("asyncio").setLevel("WARNING")
    logging.getLogger("pika").setLevel("WARNING")
    logging.getLogger("stomp").setLevel("WARNING")
    logging.getLogger("luigi-interface").setLevel("WARNING")
    logging.getLogger("luigi.xchembku_scheduler").setLevel("INFO")
    logging.getLogger("urllib3.connectionpool").setLevel("INFO")

    logging.getLogger("xchembku_lib.things").setLevel("INFO")

    # Messages about starting and stopping services.
    logging.getLogger("xchembku_lib.base_aiohttp").setLevel("INFO")

    # All xchembku database sql commands.
    # logging.getLogger("dls_normsql.aiosqlite").setLevel("INFO")

    logging.getLogger("xchembku_lib.xchembku_contexts.classic").setLevel("INFO")
    logging.getLogger("xchembku_lib.xchembku_datafaces.context").setLevel("INFO")

    # Registering signal handler.
    logging.getLogger("dls_siggy_lib.signal").setLevel("INFO")

    # Cover the version.
    # logger.info("\n%s", (json.dumps(version_meta(), indent=4)))

    yield None


# --------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def output_directory(request):
    # TODO: Better way to get a newline in conftest after pytest emits the test class name.
    print("")

    # Tmp directory which we can write into.
    output_directory = "/tmp/%s/%s/%s" % (
        "/".join(__file__.split("/")[-3:-1]),
        request.cls.__name__,
        request.function.__name__,
    )

    # Tmp directory which we can write into.
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory, ignore_errors=False, onerror=None)
    os.makedirs(output_directory)

    # logger.debug("output_directory is %s" % (output_directory))

    yield output_directory
