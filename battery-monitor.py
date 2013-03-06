#!/bin/python

import serial
import time, sys

serial_port = '/dev/ttyUSB.BK5491B'

ser = serial.Serial()

ser.port = serial_port
ser.baudrate = 38400
ser.timeout=0.08
ser.open()

try:
  if True:
    ser.write("*RST\n")
    time.sleep(5)


  if True:
    ser.write("FUNC CURR:DC\r")
    time.sleep(0.5)
    ser.write("TRIG:SOUR BUS\r")
    time.sleep(0.5)
    ser.write("TRIG:SOUR?\r")
    time.sleep(0.5)
    print(ser.read(100))
    ser.write("CURR:DC:NPLC 0.1\n")
    time.sleep(0.5)
    ser.write("CURR:DC:RANGE 0.05\n")
    print(ser.read(100))

  delay = 0.05
  last_time = time.time()
  count = 0
  total_charge = 0
  total_current = 0
  total_time = 0
  battery_charge = 140

  # ser.write("*TRG\r")
  while True:
    time.sleep(delay)
    ser.write("FETC?;*TRG\r")

    current_time = time.time()
    time_delta = (current_time - last_time)
    last_time = current_time

    result = ser.readline().strip()
    try:
      current_ma = float(result)*1000
      count = count + 1
      #charge_mah = current_ma * time_delta / 3600

      total_current = total_current + current_ma
      total_time = total_time + time_delta

      battery_life = battery_charge / (total_current/count)

      total_charge = (total_current/count) * (total_time/(60*60))

      # print("%f, %f" % (time_delta, current_ma))
      # print("charge_used: %f mAh\tbattery_life: %f h or %f d" % (total_charge, battery_life, battery_life/24))
      print("%f %f %f %f" % (current_time,current_ma, total_charge, battery_life))
    except ValueError:
      print("Oops! Unable to parse response: %s" % (result))
      ser.write("SYST:ERR?\r")
      print("Error status: %s" % ser.readline())
      time.sleep(1.5) # wait for the error to go away

  # ser.write("*TRG\r")
except KeyboardInterrupt:
  time.sleep(1)
  ser.write("*RST\n")
  time.sleep(5)
  ser.close()
  print("Bye")

ser.close()
