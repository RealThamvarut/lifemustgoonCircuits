import lgpio
import time

# BCM GPIO numbers (not physical pins!)
RED = 17     # physical pin 33
YELLOW = 27   # physical pin 31
GREEN = 22    # physical pin 29

# Open gpiochip0 (main GPIO controller)
gpioController = lgpio.gpiochip_open(0)

# Claim the lines as outputs
lgpio.gpio_claim_output(gpioController, RED)
lgpio.gpio_claim_output(gpioController, YELLOW)
lgpio.gpio_claim_output(gpioController, GREEN)

try:
    while True:
        # Red ON
        lgpio.gpio_write(gpioController, RED, 1)
        time.sleep(1)
        lgpio.gpio_write(gpioController, RED, 0)

        # Yellow ON
        lgpio.gpio_write(gpioController, YELLOW, 1)
        time.sleep(1)
        lgpio.gpio_write(gpioController, YELLOW, 0)

        # Green ON
        lgpio.gpio_write(gpioController, GREEN, 1)
        time.sleep(1)
        lgpio.gpio_write(gpioController, GREEN, 0)

except KeyboardInterrupt:
    pass
finally:
    lgpio.gpiochip_close(gpioController)