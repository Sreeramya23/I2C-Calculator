# I2C Calculator

[TOC]

## Purpose
- **Tkinter GUI to calculate standard pull-up resistances for I2C protocol.**

## Features
- Supports calculation for the following modes;
  - Standard
  - Fast
  - Fast plus

## Formulas

> R<sub>p</sub>(min) = ( V<sub>dd</sub> - V<sub>ol</sub>(max) ) / I<sub>ol</sub> (max)

1. R<sub>p</sub>(min) - Minimum value of pullup resistance (Ohms)
2. V<sub>dd</sub> - Line voltage (V)
3. V<sub>ol</sub>(max) - Max output voltage of SDA/SCL lines (0.4 V)
4. I<sub>ol</sub> - Max Output current of SDA/SCL lines (3 mA)

> R<sub>p</sub>(max) = ( t<sub>rise</sub> ) / (0.8473 x C<sub>b</sub>)

1. R<sub>p</sub>(max) - max value of pullup resistance (Ohms)
2. t<sub>rise</sub>  - Time to rise from 30% to 70% of V<sub>dd</sub> (See I2C specs) (ns)
3. C<sub>b</sub> - Net Bus Capacitance (See I2C specs) (pF)

## Requirements

- Please see requirements.txt

## Usage

1. pip3 install -r requirements.txt
2. python3 I2C_Calculator.py
