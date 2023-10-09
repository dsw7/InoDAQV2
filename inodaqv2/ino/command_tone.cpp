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

    if ((pin < 2) or (pin > 13))
    {
        Helpers::error(F("Must select a digital pin between 2 and 13!"));
        return;
    }

    int freq = command.substring(idx_freq + 1).toInt();

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

    static int pin_to_no_tone = -1;
    ::String str_pin_to_no_tone = ::String(pin_to_no_tone);

    if (pin_to_no_tone != -1)
    {
        // See https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/
        // See https://www.arduino.cc/reference/en/language/functions/advanced-io/notone/
        ::noTone(pin_to_no_tone);
    }

    ::tone(pin, freq);
    pin_to_no_tone = pin;

    // Return payload of form: "1;<pin>,<frequency>,<pin-that-was-noTone()-ed>"

    ::String msg = ::String(pin) + "," + ::String(freq) + "," + str_pin_to_no_tone;
    Helpers::info(msg);
}

} // Command
