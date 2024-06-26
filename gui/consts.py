from logging import getLogger
import re

LOGGER = getLogger("inodaqv2")

PAT_VALID_AREAD = re.compile(r"^1;\d{1,4},\d{1,4},\d{1,4},\d{1,4},\d{1,4},\d{1,4}$")
PAT_VALID_DIG = re.compile(r"^1;\d{1,2},(on|off)$")
PAT_VALID_DREAD = re.compile(r"^1;\d{1},\d{1},\d{1},\d{1},\d{1},\d{1}$")
PAT_VALID_PWM = re.compile(r"^1;\d{1,2},\d{1,3}$")
PAT_VALID_TONE = re.compile(r"^1;\d{1},\d{1,5}$")

MARGIN_X = 10
MARGIN_Y = 15
PADDING_FRAME = 5
