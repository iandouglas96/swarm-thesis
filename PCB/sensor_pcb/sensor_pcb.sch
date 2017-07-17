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
LIBS:sensor_pcb-cache
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
L CONN_01X03 P1
U 1 1 5942FAE2
P 6050 4450
F 0 "P1" H 6050 4650 50  0000 C CNN
F 1 "CONN_01X03" V 6150 4450 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_1x03_Pitch2.54mm" H 6050 4450 50  0001 C CNN
F 3 "" H 6050 4450 50  0000 C CNN
	1    6050 4450
	0    1    1    0   
$EndComp
Wire Wire Line
	6200 3700 6200 4250
Wire Wire Line
	6200 4250 6150 4250
Wire Wire Line
	5850 3700 6200 3700
Wire Wire Line
	5950 4250 5450 4250
Wire Wire Line
	5450 4250 5450 3700
Wire Wire Line
	6050 4250 6050 4000
Wire Wire Line
	6050 4000 6600 4000
Wire Wire Line
	6600 4000 6600 3700
$Comp
L BUT11A Q1
U 1 1 596CC2BE
P 5650 3800
F 0 "Q1" H 5900 3875 50  0000 L CNN
F 1 "BUT11A" H 5900 3800 50  0000 L CNN
F 2 "TO_SOT_Packages_THT:TO-18-4_Lens" H 5900 3725 50  0000 L CIN
F 3 "" H 5650 3800 50  0000 L CNN
	1    5650 3800
	0    -1   -1   0   
$EndComp
$Comp
L BUT11A Q?
U 1 1 596CC336
P 6400 3600
F 0 "Q?" H 6650 3675 50  0000 L CNN
F 1 "BUT11A" H 6650 3600 50  0000 L CNN
F 2 "TO_SOT_Packages_THT:TO-18-4_Lens" H 6650 3525 50  0000 L CIN
F 3 "" H 6400 3600 50  0000 L CNN
	1    6400 3600
	0    1    1    0   
$EndComp
$EndSCHEMATC
