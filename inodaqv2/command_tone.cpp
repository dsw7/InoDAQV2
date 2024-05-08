#include "command_tone.h"

#include "helpers.h"

namespace Command
{

void command_tone(const ::String &command)
{
    // Parse command of form: "tone:<2-13>:<frequency>"

    int idx_pin = command.indexOf(':');
    int idx_freq = command.indexOf(':', idx_pin + 1);

    if (idx_freq < 0)
    {
        Helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_freq).toInt();

    if (pin == 0)
    {
        Helpers::error(F("Malformed command. Could not parse digital pin!"));
        return;
    }

    static int valid_tone_pins[4] = {2, 4, 7, 8};
    bool is_invalid_pin = true;

    for (unsigned int i = 0; i < 4; ++i)
    {
        if (valid_tone_pins[i] == pin)
        {
            is_invalid_pin = false;
        }
    }

    if (is_invalid_pin)
    {
        Helpers::error(F("Tone pin must be one of 2, 4, 7 or 8"));
        return;
    }

    long freq = command.substring(idx_freq + 1).toInt();

    if (freq == 0)
    {
        Helpers::error(F("Malformed command. Could not parse frequency!"));
        return;
    }

    if ((freq < 31) or (freq > 65535))
    {
        Helpers::error(F("Frequency must be between 31 and 65535 Hz"));
        return;
    }

    Helpers::disable_tone();
    ::tone(pin, freq);

    // Return payload of form: "1;<pin>,<frequency>"

    ::String msg = ::String(pin) + "," + ::String(freq);
    Helpers::info(msg);
}

} // namespace Command
