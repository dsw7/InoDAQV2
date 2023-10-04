#include "command_dread.h"

#include "helpers.h"

#include "Arduino.h"

namespace Command
{

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

} // Command
