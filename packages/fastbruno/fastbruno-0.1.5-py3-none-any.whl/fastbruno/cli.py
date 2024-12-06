import argparse
import importlib
import os
import sys

from fastbruno import FastBruno
from fastbruno.__internal.fastapi import FastAPI
from fastbruno.__internal.logger import bruno_logger


def fastbruno_cli():
    # dynamically import the app
    parser = argparse.ArgumentParser(
        description="Generate Bruno Files for a FastAPI app"
    )
    parser.add_argument("app_dir", type=str, help="The directory of the FastAPI app")
    args = parser.parse_args()

    if ":" not in args.app_dir:
        bruno_logger.error(
            "App directory must be in the format <module>:<app_instance>. eg: fastbruno.main:app"
        )
        sys.exit(1)

    bruno_logger.debug(f"CWD: {os.getcwd()}")

    sys.path.append(os.getcwd())

    app_path, app_instance = args.app_dir.split(":")
    try:
        fastapi_module = importlib.import_module(app_path)
        fastapi_app = getattr(fastapi_module, app_instance)
        if not isinstance(fastapi_app, FastAPI):
            bruno_logger.error("App instance is not a FastAPI app")
            sys.exit(1)
        bruno_logger.info("Brunofying FastAPI Routes...")
        FastBruno(fastapi_app).brunofy()

        bruno_logger.info("Bruno files generated successfully at ./bruno")
    except AttributeError as e:
        bruno_logger.error(f"App instance not found: {e}", exc_info=True)
        sys.exit(1)
    except ImportError as e:
        bruno_logger.error(f"Error importing app: {e}", exc_info=True)
        sys.exit(1)
