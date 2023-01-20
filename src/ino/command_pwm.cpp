#include "command_pwm.h"

#include "helpers.h"

namespace Command
{

void command_pwm(const ::String &command)
{
    // Parse command of form: "pwm:<3|5|6|9|10|11>:<0-255>"

    int idx_pin = command.indexOf(':');
    int idx_duty_cycle = command.indexOf(':', idx_pin + 1);

    if (idx_duty_cycle < 0)
    {
        Helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_duty_cycle).toInt();

    if (pin == 0)
    {
        Helpers::error(F("Malformed command. Could not parse digital pin!"));
        return;
    }

    static int valid_pwm_pins[6] = {3, 5, 6, 9, 10, 11};
    bool is_invalid_pin = true;

    for (unsigned int i = 0; i < 6; ++i)
    {
        if (valid_pwm_pins[i] == pin)
        {
            is_invalid_pin = false;
        }
    }

    if (is_invalid_pin)
    {
        Helpers::error(F("Digital pin must be one of 3, 5, 6, 9, 10 or 11"));
        return;
    }

    ::String raw_duty_cycle = command.substring(idx_duty_cycle + 1);
    int duty_cycle = 0;

    if (not raw_duty_cycle.equals("0"))
    {
        duty_cycle = raw_duty_cycle.toInt();

        if (duty_cycle == 0)
        {
            Helpers::error(F("Could not parse duty cycle!"));
            return;
        }
    }

    if ((duty_cycle < 0) or (duty_cycle > 255))
    {
        Helpers::error(F("Duty cycle must be between 0 and 255"));
        return;
    }

    ::analogWrite(pin, duty_cycle);

    ::String msg = "Pin " + ::String(pin) + " emitting PWM wave with duty cycle of " + ::String(duty_cycle);
    Helpers::info(msg);
}

} // Command
