#include "command_ping.h"

#include "helpers.h"

#include "Arduino.h"

namespace Command
{

void command_ping() {

    static bool status = false;

    status = !status;
    ::digitalWrite(LED_BUILTIN, status);

    if (status)
    {
        Helpers::info(F("Built in LED is ON"));
        return;
    }

    Helpers::info(F("Built in LED is OFF"));
}

} // Command
