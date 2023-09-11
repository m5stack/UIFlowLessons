import machine

class SN74HC595:
  ds = None
  st = None
  sh = None
  ready = False

  def __init__(self, ds, st, sh):
    self.ds = machine.Pin(ds, mode=machine.Pin.OUT, pull=0x00)
    self.st = machine.Pin(st, mode=machine.Pin.OUT, pull=0x00)
    self.sh = machine.Pin(sh, mode=machine.Pin.OUT, pull=0x00)
    self.ready = True

  def Raw(self, value):
    if self.ready == True:
      self.ds.value(0)
      for i in range(8):
        self.sh.value((value >> (7 - i)) & 1)
        self.st.value(1)
        self.st.value(0)
      self.ds.value(1)

  def Text(self, value, alphabet, delay = 250):
    if self.ready == True:
      length = len(value)
      for i in range(length):
        symbol = value[i]
        if symbol == '.':
          continue
        if symbol in alphabet.keys():
          if i < length - 1 and value[i + 1] == '.':
            self.Raw(alphabet[value[i]] | alphabet['.'])
          else:
            self.Raw(alphabet[value[i]])
          wait_ms(delay)
