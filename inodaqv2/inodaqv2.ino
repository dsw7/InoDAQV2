#include "commands.hpp"
#include "command_dig.h"
#include "command_dread.h"
#include "command_ping.h"
#include "command_pwm.h"
#include "command_tone.h"
#include "helpers.h"

void setup()
{
    unsigned int baud_rate = 9600;
    ::Serial.begin(baud_rate);

    unsigned int max_time_millisec_wait_serial_data = 10;
    ::Serial.setTimeout(max_time_millisec_wait_serial_data);

    ::pinMode(LED_BUILTIN, OUTPUT);

    for (unsigned int pin = 2; pin <= 13; pin++)
    {
        ::pinMode(pin, OUTPUT);
        ::digitalWrite(pin, LOW);
    }

    ::pinMode(A0, INPUT);
    ::pinMode(A1, INPUT);
    ::pinMode(A2, INPUT);
    ::pinMode(A3, INPUT);
    ::pinMode(A4, INPUT);
    ::pinMode(A5, INPUT);
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
            ::command_dig(command);
        }
        else if (command.startsWith(F("pwm:")))
        {
            Command::command_pwm(command);
        }
        else if (command == F("aread"))
        {
            ::command_aread();
        }
        else if (command == F("dread"))
        {
            Command::command_dread();
        }
        else if (command.startsWith(F("tone:")))
        {
            Command::command_tone(command);
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
