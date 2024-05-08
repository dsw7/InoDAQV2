#pragma once

#include "Arduino.h"

namespace helpers
{
void info(const ::String &message);
void error(const ::String &message);
void disable_tone();
} // namespace helpers
