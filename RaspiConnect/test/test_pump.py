import lgpio
import time

CHIP = 0
PUMP_PIN = 5       # output
BUTTON_PIN = 16    # input

h = lgpio.gpiochip_open(CHIP)

# Pump = output
lgpio.gpio_claim_output(h, PUMP_PIN)

# Button = input (with internal pull-down)
lgpio.gpio_claim_input(h, BUTTON_PIN, lgpio.SET_PULL_UP)

try:
    while True:
        val = lgpio.gpio_read(h, BUTTON_PIN)

        # Button pressed = logic LOW (because pull-up)
        if val == 0:
            lgpio.gpio_write(h, PUMP_PIN, 1)
        else:
            lgpio.gpio_write(h, PUMP_PIN, 0)

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

lgpio.gpiochip_close(h)
