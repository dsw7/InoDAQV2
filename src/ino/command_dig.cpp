#include "command_dig.h"

#include "helpers.h"

namespace Command
{

void command_toggle_digital_pin(const ::String &command)
{
    // Parse command of form: "dig:<2-13>:<on/off>"

    int idx_pin = command.indexOf(':');
    int idx_state = command.indexOf(':', idx_pin + 1);

    if (idx_state < 0)
    {
        Helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_state).toInt();

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

    unsigned int idx_arr_pins = pin - 2;

    static bool pins[12] = {
        false, // pin 2
        false, // pin 3
        false, // ...
        false,
        false,
        false,
        false,
        false,
        false,
        false, // ...
        false, // pin 12
        false  // pin 13
    };

    ::String state = command.substring(idx_state + 1, command.length());

    if (state.equals(F("on")))
    {
        pins[idx_arr_pins] = true;
    }
    else if (state.equals(F("off")))
    {
        pins[idx_arr_pins] = false;
    }
    else
    {
        Helpers::error(F("Valid states are 'on' and 'off'"));
        return;
    }

    ::digitalWrite(pin, pins[idx_arr_pins]);

    ::String msg = "Pin " + ::String(pin) + " set to " + state;
    Helpers::info(msg);
}

} // Command
