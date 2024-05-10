#include "commands.hpp"

#include "helpers.hpp"

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

    helpers::info(msg);
}

void command_dig(const ::String &command)
{
    // Parse command of form: "dig:<2-13>:<on|off>"

    int idx_pin = command.indexOf(':');
    int idx_state = command.indexOf(':', idx_pin + 1);

    if (idx_state < 0)
    {
        helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_state).toInt();

    if (pin == 0)
    {
        helpers::error(F("Malformed command. Could not parse digital pin!"));
        return;
    }

    if ((pin < 2) or (pin > 13))
    {
        helpers::error(F("Must select a digital pin between 2 and 13!"));
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
        helpers::error(F("Valid states are 'on' and 'off'"));
        return;
    }

    // Return payload of form: "1;<pin>,<on|off>"

    ::String msg = ::String(pin) + "," + state;
    helpers::info(msg);
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

    helpers::info(msg);
}

void command_ping()
{
    static bool status = false;

    status = !status;
    ::digitalWrite(LED_BUILTIN, status);

    if (status)
    {
        helpers::info(F("Built in LED is ON"));
        return;
    }

    helpers::info(F("Built in LED is OFF"));
}

void disable_tone()
{
    // Tone needs to be disabled to free the pin for other uses
    // See https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/
    static int valid_tone_pins[4] = {2, 4, 7, 8};

    for (unsigned int i = 0; i < 4; ++i)
    {
        ::noTone(valid_tone_pins[i]);
    }
}

void command_pwm(const ::String &command)
{
    // Parse command of form: "pwm:<3|5|6|9|10|11>:<0-255>"

    int idx_pin = command.indexOf(':');
    int idx_duty_cycle = command.indexOf(':', idx_pin + 1);

    if (idx_duty_cycle < 0)
    {
        helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_duty_cycle).toInt();

    if (pin == 0)
    {
        helpers::error(F("Malformed command. Could not parse digital pin!"));
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
        helpers::error(F("Digital pin must be one of 3, 5, 6, 9, 10 or 11"));
        return;
    }

    ::String raw_duty_cycle = command.substring(idx_duty_cycle + 1);
    int duty_cycle = 0;

    if (not raw_duty_cycle.equals("0"))
    {
        duty_cycle = raw_duty_cycle.toInt();

        if (duty_cycle == 0)
        {
            helpers::error(F("Could not parse duty cycle!"));
            return;
        }
    }

    if ((duty_cycle < 0) or (duty_cycle > 255))
    {
        helpers::error(F("Duty cycle must be between 0 and 255"));
        return;
    }

    // Tone on any pin will interfere with PWM on pins 3 and 11
    // See https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/
    ::disable_tone();
    ::analogWrite(pin, duty_cycle);

    // Return payload of form: "1;<pin>,<duty-cycle>"

    ::String msg = ::String(pin) + "," + ::String(duty_cycle);
    helpers::info(msg);
}

void command_tone(const ::String &command)
{
    // Parse command of form: "tone:<2-13>:<frequency>"

    int idx_pin = command.indexOf(':');
    int idx_freq = command.indexOf(':', idx_pin + 1);

    if (idx_freq < 0)
    {
        helpers::error(F("Malformed command. Missing second colon!"));
        return;
    }

    int pin = command.substring(idx_pin + 1, idx_freq).toInt();

    if (pin == 0)
    {
        helpers::error(F("Malformed command. Could not parse digital pin!"));
        return;
    }

    static int valid_tone_pins[4] = {2, 4, 7, 8};
    bool is_invalid_pin = true;

    for (unsigned int i = 0; i < 4; ++i)
    {
        if (valid_tone_pins[i] == pin)
        {
            is_invalid_pin = false;
        }
    }

    if (is_invalid_pin)
    {
        helpers::error(F("Tone pin must be one of 2, 4, 7 or 8"));
        return;
    }

    long freq = command.substring(idx_freq + 1).toInt();

    if (freq == 0)
    {
        helpers::error(F("Malformed command. Could not parse frequency!"));
        return;
    }

    if ((freq < 31) or (freq > 65535))
    {
        helpers::error(F("Frequency must be between 31 and 65535 Hz"));
        return;
    }

    ::disable_tone();
    ::tone(pin, freq);

    // Return payload of form: "1;<pin>,<frequency>"

    ::String msg = ::String(pin) + "," + ::String(freq);
    helpers::info(msg);
}
