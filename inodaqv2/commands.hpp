#pragma once

#include "Arduino.h"

namespace commands {
void command_aread();
void command_dig(const String &command);
void command_dread();
void command_ping();
void command_pwm(const String &command);
void command_tone(const String &command);
} // namespace commands
