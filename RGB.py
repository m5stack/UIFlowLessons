class RGB:
  def __init__(self, pin_number=35, led_numbers=1):
    self.pinNumber = pin_number
    self.ledNumbers = led_numbers
    self.ledPin = None
    self.ledDriver = None

    self.init_led()

  def init_led(self):
    self.ledPin = Pin(self.pinNumber, mode=Pin.OUT)
    self.ledDriver = NeoPixel(self.ledPin, self.ledNumbers)
    self.ledDriver.br = 100

  def fill_color(self, color):
    color_rgb = self.ledDriver.color_to_rgb(color)
    self.ledDriver.fill(color_rgb)
    self.ledDriver.write()
