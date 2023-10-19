#include "helpers.h"

namespace Helpers
{

void info(const ::String &message)
{
    ::Serial.println("1;" + message);
    ::Serial.flush();
}

void error(const ::String &message)
{
    ::Serial.println("0;" + message);
    ::Serial.flush();
}

void disable_tone()
{
    // Tone needs to be disabled to free the pin for other uses
    // See https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/
    for (unsigned int pin = 2; pin < 14; ++pin)
    {
        ::noTone(pin);
    }
}

} // namespace Helpers
