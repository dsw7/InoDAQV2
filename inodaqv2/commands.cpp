#include "commands.hpp"

#include "helpers.h"

void command_aread()
{
    ::String msg = ::String(::analogRead(A0));

    msg += ',';
    msg += ::String(::analogRead(A1));
    msg += ',';
    msg += ::String(::analogRead(A2));
    msg += ',';
    msg += ::String(::analogRead(A3));
    msg += ',';
    msg += ::String(::analogRead(A4));
    msg += ',';
    msg += ::String(::analogRead(A5));

    Helpers::info(msg);
}

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
        // An existing tone will block a digitalWrite
        ::noTone(pin);
        ::digitalWrite(pin, HIGH);
    }
    else if (state.equals(F("off")))
    {
        ::noTone(pin);
        ::digitalWrite(pin, LOW);
    }
    else
    {
        Helpers::error(F("Valid states are 'on' and 'off'"));
        return;
    }

    // Return payload of form: "1;<pin>,<on|off>"

    ::String msg = ::String(pin) + "," + state;
    Helpers::info(msg);
}

void command_dread()
{
    ::String msg = ::String(::digitalRead(A0));

    msg += ',';
    msg += ::String(::digitalRead(A1));
    msg += ',';
    msg += ::String(::digitalRead(A2));
    msg += ',';
    msg += ::String(::digitalRead(A3));
    msg += ',';
    msg += ::String(::digitalRead(A4));
    msg += ',';
    msg += ::String(::digitalRead(A5));

    Helpers::info(msg);
}
