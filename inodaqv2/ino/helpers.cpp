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
    static int valid_tone_pins[4] = {2, 4, 7, 8};

    for (unsigned int i = 0; i < 4; ++i)
    {
        ::noTone(valid_tone_pins[i]);
    }
}

} // namespace Helpers
