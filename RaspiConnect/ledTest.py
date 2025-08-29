import gpiod
import time

RED_LED_PIN = 33
GREEN_LED_PIN = 29
YELLOW_LED_PIN = 31

chip = gpiod.Chip('gpiochip4')

red_led_line = chip.get_line(RED_LED_PIN)
green_led_line = chip.get_line(GREEN_LED_PIN)
yellow_led_line = chip.get_line(YELLOW_LED_PIN)

red_led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
green_led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
yellow_led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        # Example traffic light sequence
        red_led_line.set_value(1)
        time.sleep(1)
        red_led_line.set_value(0)

        yellow_led_line.set_value(1)
        time.sleep(1)
        yellow_led_line.set_value(0)

        green_led_line.set_value(1)
        time.sleep(1)
        green_led_line.set_value(0)

finally:
    red_led_line.release()
    yellow_led_line.release()
    green_led_line.release()
