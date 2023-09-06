#include "command_dig.h"

#include "helpers.h"

namespace Command
{

void command_dig(const ::String &command)
{
    // Parse command of form: "dig:<2-13>:<on|off>"

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

    ::String state = command.substring(idx_state + 1);

    if (state.equals(F("on")))
    {
        ::digitalWrite(pin, HIGH);
    }
    else if (state.equals(F("off")))
    {
        ::digitalWrite(pin, LOW);
    }
    else
    {
        Helpers::error(F("Valid states are 'on' and 'off'"));
        return;
    }

    ::String msg = "Pin " + ::String(pin) + " set to " + state;

    Helpers::info(msg);
}

} // Command
