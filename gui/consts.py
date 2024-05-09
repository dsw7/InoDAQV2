from logging import getLogger
import re

LOGGER = getLogger("inodaqv2")
PAT_VALID_DIG = re.compile(r"^1;\d{1,2},(on|off)$")
