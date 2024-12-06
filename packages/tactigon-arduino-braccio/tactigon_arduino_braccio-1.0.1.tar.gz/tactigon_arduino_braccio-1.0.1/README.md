# Tactigon Arduino Braccio

![The tactigon team](https://avatars.githubusercontent.com/u/63020285?s=200&v=4)

This package enables to comunicate with Arduino Braccio using a Bluetooth to UART device such as Adafruit Bluefruit LE Uart.

This package can be used alongside with [Tactigon Gear](https://pypi.org/project/tactigon-gear/) and [Tactigon Speech](https://pypi.org/project/tactigon-speech/) libraries to drive the Braccio robot using gesture and "edge" voice command detection.


## Prerequisites
In order to use the Tactigon Arduino Braccio library you need:

* Python version: following versions has been used and tested. It is STRONGLY recommended to use these ones depending on platform.
  * Win10: 3.8.7

## Installing

Install and update using pip:

`pip install tactigon-arduino-braccio`

## A Simple Example

```python
import time

from tactigon_arduino_braccio import Braccio, BraccioConfig, Wrist, Gripper

if __name__ == "__main__":
    cfg = BraccioConfig("D1:EF:85:90:07:DE")

    with Braccio(cfg) as braccio:

        print("Connecting...")
        while not braccio.connected:
            time.sleep(0.1)

        print("Connected!")
        
        x = 120
        y = 50
        z = 20
        wrist = Wrist.HORIZONTAL
        gripper = Gripper.OPEN
        res, status, time = braccio.move(x, y, z, wrist, gripper)

        print(res, status, time)

    print("disconnected")

```

## Links
- [Arduino code](https://github.com/TactigonTeam/Tactigon-SDK/blob/main/examples/arduino_braccio/arduino_code/braccio.ino)
- [Solver](https://github.com/NNaert/Python-controlled-Braccio-robot-arm)
- [Tactigon integration](https://github.com/TactigonTeam/Tactigon-SDK)