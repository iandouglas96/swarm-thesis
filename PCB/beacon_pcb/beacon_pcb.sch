EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L LED D1
U 1 1 5942F5A8
P 5450 3350
F 0 "D1" H 5450 3450 50  0000 C CNN
F 1 "LED" H 5450 3250 50  0000 C CNN
F 2 "LEDs:LED_D3.0mm" H 5450 3350 50  0001 C CNN
F 3 "" H 5450 3350 50  0000 C CNN
	1    5450 3350
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X02 P1
U 1 1 5942F620
P 5450 3950
F 0 "P1" H 5450 4100 50  0000 C CNN
F 1 "CONN_01X02" V 5550 3950 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 5450 3950 50  0001 C CNN
F 3 "" H 5450 3950 50  0000 C CNN
	1    5450 3950
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 3750 5500 3650
Wire Wire Line
	5500 3650 5650 3650
Wire Wire Line
	5650 3650 5650 3350
Wire Wire Line
	5400 3750 5400 3650
Wire Wire Line
	5400 3650 5250 3650
Wire Wire Line
	5250 3650 5250 3350
$EndSCHEMATC
