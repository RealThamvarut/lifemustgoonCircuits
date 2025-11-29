import lgpio
import time

CHIP = 0               # usually 0 on all Raspberry Pis
BUTTON_PIN = 16       # GPIO number, not pin number

h = lgpio.gpiochip_open(CHIP)

# configure as input with internal pull-down disabled because we use external resistor
lgpio.gpio_claim_input(h, BUTTON_PIN)

try:
    while True:
        val = lgpio.gpio_read(h, BUTTON_PIN)
        print("Pressed" if val == 1 else "Released")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

lgpio.gpiochip_close(h)
