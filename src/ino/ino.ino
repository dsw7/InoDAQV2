#include "command_ping.h"
#include "command_toggle_digital_pin.h"
#include "helpers.h"

void setup()
{
    unsigned int baud_rate = 9600;
    ::Serial.begin(baud_rate);

    unsigned int max_time_millisec_wait_serial_data = 10;
    ::Serial.setTimeout(max_time_millisec_wait_serial_data);

    ::pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    while (::Serial.available() > 0)
    {
        ::String command = ::Serial.readString();
        command.trim();

        if (command == F("hello"))
        {
            Helpers::info(F("Hello from InoDAQV2"));
        }
        else if (command == F("ping"))
        {
            Command::command_ping();
        }
        else if (command.startsWith(F("dig:")))
        {
            Command::command_toggle_digital_pin(command);
        }
        else if (command == F("exit"))
        {
            Helpers::info(F("Closing connection. Goodbye!"));
            ::Serial.end();
            break;
        }
        else
        {
            Helpers::error("Unknown command: " + command);
        }
    }
}
