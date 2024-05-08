#include "command_aread.h"

#include "helpers.h"

#include "Arduino.h"

namespace Command
{

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

} // namespace Command
