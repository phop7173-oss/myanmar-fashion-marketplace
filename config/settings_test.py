# Purpose: settings used only by pytest. Forces development mode so test results do not
# depend on the developer's shell variables (CODE-STYLE: deterministic tests).
import os

os.environ["APP_ENV"] = "development"
os.environ.pop("SECRET_KEY", None)
os.environ.pop("ALLOWED_HOSTS", None)

from config.settings import *  # noqa: E402, F403
