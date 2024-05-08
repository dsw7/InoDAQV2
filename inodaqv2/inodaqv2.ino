#include "commands.hpp"
#include "helpers.hpp"

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
            helpers::info(F("Hello from InoDAQV2"));
        }
        else if (command == F("ping"))
        {
            ::command_ping();
        }
        else if (command.startsWith(F("dig:")))
        {
            ::command_dig(command);
        }
        else if (command.startsWith(F("pwm:")))
        {
            ::command_pwm(command);
        }
        else if (command == F("aread"))
        {
            ::command_aread();
        }
        else if (command == F("dread"))
        {
            ::command_dread();
        }
        else if (command.startsWith(F("tone:")))
        {
            ::command_tone(command);
        }
        else if (command == F("exit"))
        {
            helpers::info(F("Closing connection. Goodbye!"));
            ::Serial.end();
            break;
        }
        else
        {
            helpers::error("Unknown command: " + command);
        }
    }
}
