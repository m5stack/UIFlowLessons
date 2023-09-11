from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import time
import machine
import ntptime
from easyIO import *




myAlphabet = None
timeNow = None







import machine

class SN74HC595:
  ds = None # Data
  st = None # Latch
  sh = None # Clock
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

shiftRegister1 = SN74HC595(22, 19, 23)

myAlphabet = {'0':0b1101111,'1':0b1010,'2':0b11100110,'3':0b11001110,'4':0b10001011,'5':0b11001101,'6':0b11101101,'7':0b1110,'8':0b11101111,'9':0b11001111,'.':0b10000}
wifiCfg.autoConnect(lcdShow=False)
for count in range(60):
  wait(1)
  if wifiCfg.wlan_sta.isconnected():
    break
if not (wifiCfg.wlan_sta.isconnected()):
  machine.reset()
ntp = ntptime.client(host='hk.pool.ntp.org', timezone=7)
while True:
  timeNow = (ntp.formatTime('.')).split('.')
  digitalWrite(33, 1)
  shiftRegister1.Text((str(timeNow[-1]) + str('.')), myAlphabet, 750)

  digitalWrite(33, 0)
  digitalWrite(21, 1)
  shiftRegister1.Text((str(timeNow[0]) + str('.')), myAlphabet, 750)

  digitalWrite(21, 0)
  digitalWrite(25, 1)
  shiftRegister1.Text((str(timeNow[1]) + str('.')), myAlphabet, 750)

  digitalWrite(25, 0)
  wait_ms(2)
