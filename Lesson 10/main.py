from m5stack import *
from m5ui import *
from uiflow import *

import network
import socket
import urllib.parse

new_mac = bytearray([0x10, 0x20, 0x30, 0x40, 0x50, 0x60])

# STA
sta_ssid = "Free WiFi Hotspot"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.disconnect()
sta_if.config(mac=new_mac)
sta_if.active(True)
sta_if.connect(sta_ssid)

while not sta_if.isconnected():
  pass

print("Wi-Fi Connected: ", sta_ssid)
print("IP: ", sta_if.ifconfig()[0])

# SoftAP
ap_ssid = "CaptivePortalBridge"
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid=ap_ssid)

proxyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxyServer.bind(('0.0.0.0', 8080))
proxyServer.listen(10)

while True:
  try:
    APSocket, addr = proxyServer.accept()
    APSocket.setblocking(False)
    APSocket.settimeout(3)

    print("A new connection has been accepted at address: ", addr)

    APSocketData = APSocket.recv(2048)

    if not APSocketData:
      print("The connection did not provide incoming data. Closing.")
      APSocket.close()
      continue

    APSocketDataString = APSocketData.decode('utf-8')
    APSocketDataStringLines = APSocketDataString.split('\r\n')
    APSocketDataStringFirstLine = APSocketDataStringLines[0].split(' ')

    typeRequest = APSocketDataStringFirstLine[0]
    print("The type of request: ", typeRequest)

    URL = APSocketDataStringFirstLine[1]
    parsedURL = urllib.parse.urlparse(URL)

    host = None
    port = None

    if parsedURL.netloc:
      netlocParts = parsedURL.netloc.split(':')
      host = netlocParts[0]
      if len(netlocParts) > 1:
        port = int(netlocParts[1])

    if not host and parsedURL.path:
      pathSplited = parsedURL.path.split(':')
      if len(pathSplited) > 1:
        host = pathSplited[0]
        port = int(pathSplited[1])

    print("Host: ", host)

    if port is None:
      port = 80

    print("Port: ", port)

    if port != 80:
      print("Closing connection to ports other than 80.")
      APSocket.close()
      continue

    if host and port:
      print("Redirecting data to a remote host.")

      STASocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      STASocket.connect((host, port))
      STASocket.setblocking(False)
      STASocket.settimeout(1)
      STASocket.sendall(APSocketData)

      while True:
        try:
          STASocketData = STASocket.recv(2048)
          STASocketDataLength = len(STASocketData)
          print("Recived ", STASocketDataLength, " bytes from STA.")
          if STASocketDataLength == 0:
            STASocket.close()
            break
          APSocket.sendall(STASocketData)
        except OSError as e:
          if "[Errno 110] ETIMEDOUT" in str(e):
            STASocket.close()
            break

    APSocket.close()

  except Exception as e:
    print('Exception:', str(e))
