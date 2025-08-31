import lgpio
import time

class Led:
    def __init__(self, RED_LED_GPIO_PIN=17, YELLOW_LED_GPIO_PIN=27, GREEN_LED_GPIO_PIN=22):
        self.gpioController = lgpio.gpiochip_open(0)
        self.led_pins = {
            'red': RED_LED_GPIO_PIN,
            'yellow': YELLOW_LED_GPIO_PIN,
            'green': GREEN_LED_GPIO_PIN
        }

        for pin in self.led_pins.values():
            lgpio.gpio_claim_output(self.gpioController, pin)

        self.setLed('yellow', 1)

    def setLed(self, color, state):
        lgpio.gpio_write(self.gpioController, self.led_pins[color], state)

    def blinkLed(self, color, delay=3):
        self.setLed(color, 1)
        time.sleep(delay)
        self.setLed(color, 0)
    
    def greenOn(self):
        self.setLed("yellow", 0)
        self.setLed("green", 1)

    def greenOff(self):
        self.setLed("green", 0)
        self.setLed("yellow", 1)

    def redOn(self, delay = 3):
        self.setLed("yellow", 0)
        self.blinkLed("red", delay)
        self.setLed("yellow", 1)