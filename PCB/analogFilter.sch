EESchema Schematic File Version 2
LIBS:main_pcb-rescue
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
LIBS:teensy_3.1
LIBS:rfm69_breakout
LIBS:tb6612_breakout
LIBS:drv8834_breakout
LIBS:main_pcb-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 3
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
L MCP6004 U3
U 1 1 5941D635
P 4100 3650
AR Path="/5941B2B4/5941D635" Ref="U3"  Part="1" 
AR Path="/5941F948/5941D635" Ref="U3"  Part="4" 
F 0 "U3" H 4150 3850 50  0000 C CNN
F 1 "MCP6004" H 4250 3450 50  0000 C CNN
F 2 "Housings_DIP:DIP-14_W7.62mm" H 4050 3750 50  0001 C CNN
F 3 "" H 4150 3850 50  0000 C CNN
	1    4100 3650
	1    0    0    -1  
$EndComp
$Comp
L MCP6004 U3
U 2 1 5941D63C
P 5400 3550
AR Path="/5941B2B4/5941D63C" Ref="U3"  Part="2" 
AR Path="/5941F948/5941D63C" Ref="U4"  Part="1" 
F 0 "U3" H 5450 3750 50  0000 C CNN
F 1 "MCP6004" H 5550 3350 50  0000 C CNN
F 2 "Housings_DIP:DIP-14_W7.62mm" H 5350 3650 50  0001 C CNN
F 3 "" H 5450 3750 50  0000 C CNN
	2    5400 3550
	1    0    0    -1  
$EndComp
$Comp
L MCP6004 U3
U 3 1 5941D643
P 6700 3450
AR Path="/5941B2B4/5941D643" Ref="U3"  Part="3" 
AR Path="/5941F948/5941D643" Ref="U4"  Part="2" 
F 0 "U3" H 6750 3650 50  0000 C CNN
F 1 "MCP6004" H 6850 3250 50  0000 C CNN
F 2 "Housings_DIP:DIP-14_W7.62mm" H 6650 3550 50  0001 C CNN
F 3 "" H 6750 3650 50  0000 C CNN
	3    6700 3450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR033
U 1 1 5941D64A
P 4000 3950
AR Path="/5941B2B4/5941D64A" Ref="#PWR033"  Part="1" 
AR Path="/5941F948/5941D64A" Ref="#PWR038"  Part="1" 
F 0 "#PWR033" H 4000 3700 50  0001 C CNN
F 1 "GND" H 4000 3800 50  0000 C CNN
F 2 "" H 4000 3950 50  0000 C CNN
F 3 "" H 4000 3950 50  0000 C CNN
	1    4000 3950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR034
U 1 1 5941D650
P 5300 3850
AR Path="/5941B2B4/5941D650" Ref="#PWR034"  Part="1" 
AR Path="/5941F948/5941D650" Ref="#PWR039"  Part="1" 
F 0 "#PWR034" H 5300 3600 50  0001 C CNN
F 1 "GND" H 5300 3700 50  0000 C CNN
F 2 "" H 5300 3850 50  0000 C CNN
F 3 "" H 5300 3850 50  0000 C CNN
	1    5300 3850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR035
U 1 1 5941D656
P 6600 3750
AR Path="/5941B2B4/5941D656" Ref="#PWR035"  Part="1" 
AR Path="/5941F948/5941D656" Ref="#PWR040"  Part="1" 
F 0 "#PWR035" H 6600 3500 50  0001 C CNN
F 1 "GND" H 6600 3600 50  0000 C CNN
F 2 "" H 6600 3750 50  0000 C CNN
F 3 "" H 6600 3750 50  0000 C CNN
	1    6600 3750
	1    0    0    -1  
$EndComp
$Comp
L R Rf1
U 1 1 5941D670
P 4150 4300
AR Path="/5941B2B4/5941D670" Ref="Rf1"  Part="1" 
AR Path="/5941F948/5941D670" Ref="Rf2"  Part="1" 
F 0 "Rf1" V 4230 4300 50  0000 C CNN
F 1 "68k" V 4150 4300 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 4080 4300 50  0001 C CNN
F 3 "" H 4150 4300 50  0000 C CNN
	1    4150 4300
	0    1    1    0   
$EndComp
$Comp
L R R1
U 1 1 5941D677
P 4700 3650
AR Path="/5941B2B4/5941D677" Ref="R1"  Part="1" 
AR Path="/5941F948/5941D677" Ref="R7"  Part="1" 
F 0 "R1" V 4780 3650 50  0000 C CNN
F 1 "20k" V 4700 3650 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 4630 3650 50  0001 C CNN
F 3 "" H 4700 3650 50  0000 C CNN
	1    4700 3650
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 5941D67F
P 5400 4150
AR Path="/5941B2B4/5941D67F" Ref="R4"  Part="1" 
AR Path="/5941F948/5941D67F" Ref="R10"  Part="1" 
F 0 "R4" V 5480 4150 50  0000 C CNN
F 1 "1M" V 5400 4150 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 5330 4150 50  0001 C CNN
F 3 "" H 5400 4150 50  0000 C CNN
	1    5400 4150
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 5941D686
P 5400 4400
AR Path="/5941B2B4/5941D686" Ref="C1"  Part="1" 
AR Path="/5941F948/5941D686" Ref="C2"  Part="1" 
F 0 "C1" H 5425 4500 50  0000 L CNN
F 1 "0.47uF" H 5425 4300 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D4.3mm_W1.9mm_P5.00mm" H 5438 4250 50  0001 C CNN
F 3 "" H 5400 4400 50  0000 C CNN
	1    5400 4400
	0    1    1    0   
$EndComp
$Comp
L R R5
U 1 1 5941D68D
P 6050 3550
AR Path="/5941B2B4/5941D68D" Ref="R5"  Part="1" 
AR Path="/5941F948/5941D68D" Ref="R11"  Part="1" 
F 0 "R5" V 6130 3550 50  0000 C CNN
F 1 "20k" V 6050 3550 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 5980 3550 50  0001 C CNN
F 3 "" H 6050 3550 50  0000 C CNN
	1    6050 3550
	0    1    1    0   
$EndComp
$Comp
L R R6
U 1 1 5941D694
P 6600 4100
AR Path="/5941B2B4/5941D694" Ref="R6"  Part="1" 
AR Path="/5941F948/5941D694" Ref="R12"  Part="1" 
F 0 "R6" V 6680 4100 50  0000 C CNN
F 1 "20k" V 6600 4100 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6530 4100 50  0001 C CNN
F 3 "" H 6600 4100 50  0000 C CNN
	1    6600 4100
	0    1    1    0   
$EndComp
$Comp
L R Rc1
U 1 1 5941D69C
P 5450 4900
AR Path="/5941B2B4/5941D69C" Ref="Rc1"  Part="1" 
AR Path="/5941F948/5941D69C" Ref="Rc2"  Part="1" 
F 0 "Rc1" V 5530 4900 50  0000 C CNN
F 1 "36k" V 5450 4900 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 5380 4900 50  0001 C CNN
F 3 "" H 5450 4900 50  0000 C CNN
	1    5450 4900
	0    1    1    0   
$EndComp
Wire Wire Line
	3700 3550 3800 3550
Wire Wire Line
	3700 3750 3800 3750
Wire Wire Line
	4000 4300 3750 4300
Wire Wire Line
	3750 3750 3750 4900
Connection ~ 3750 3750
Wire Wire Line
	4400 3650 4550 3650
Wire Wire Line
	4500 4300 4300 4300
Connection ~ 4500 3650
Wire Wire Line
	4850 3650 5100 3650
Wire Wire Line
	5000 3450 5100 3450
Wire Wire Line
	5250 4150 5050 4150
Wire Wire Line
	5050 3650 5050 4400
Connection ~ 5050 3650
Wire Wire Line
	5700 3550 5900 3550
Wire Wire Line
	5550 4150 5800 4150
Wire Wire Line
	5800 3550 5800 4400
Connection ~ 5800 3550
Wire Wire Line
	5050 4400 5250 4400
Connection ~ 5050 4150
Wire Wire Line
	5800 4400 5550 4400
Connection ~ 5800 4150
Wire Wire Line
	6200 3550 6400 3550
Wire Wire Line
	6450 4100 6300 4100
Wire Wire Line
	6300 4100 6300 3550
Connection ~ 6300 3550
Wire Wire Line
	6750 4100 7100 4100
Wire Wire Line
	6300 3350 6400 3350
Wire Wire Line
	7100 4900 5600 4900
Connection ~ 7100 4100
Wire Wire Line
	7000 3450 7100 3450
Wire Wire Line
	7100 3450 7100 4900
Wire Wire Line
	3750 4900 5300 4900
Connection ~ 3750 4300
$Comp
L GND #PWR036
U 1 1 5941E011
P 5100 2600
AR Path="/5941B2B4/5941E011" Ref="#PWR036"  Part="1" 
AR Path="/5941F948/5941E011" Ref="#PWR041"  Part="1" 
F 0 "#PWR036" H 5100 2350 50  0001 C CNN
F 1 "GND" H 5100 2450 50  0000 C CNN
F 2 "" H 5100 2600 50  0000 C CNN
F 3 "" H 5100 2600 50  0000 C CNN
	1    5100 2600
	1    0    0    -1  
$EndComp
Text HLabel 4500 2600 3    60   Input ~ 0
Vcc
Text HLabel 5100 2300 1    60   Input ~ 0
GND
Text HLabel 5900 2300 0    60   Input ~ 0
Vref
Text HLabel 3700 3750 0    60   Input ~ 0
Sen
Text HLabel 4400 3050 0    60   Input ~ 0
Out
Wire Wire Line
	4400 3050 4500 3050
Wire Wire Line
	4500 3050 4500 4300
$Comp
L R R2
U 1 1 597264A4
P 4500 2450
AR Path="/5941B2B4/597264A4" Ref="R2"  Part="1" 
AR Path="/5941F948/597264A4" Ref="R8"  Part="1" 
F 0 "R2" V 4580 2450 50  0000 C CNN
F 1 "500" V 4500 2450 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 4430 2450 50  0001 C CNN
F 3 "" H 4500 2450 50  0000 C CNN
	1    4500 2450
	1    0    0    -1  
$EndComp
$Comp
L C C4
U 1 1 59726523
P 4800 2300
AR Path="/5941B2B4/59726523" Ref="C4"  Part="1" 
AR Path="/5941F948/59726523" Ref="C6"  Part="1" 
F 0 "C4" H 4825 2400 50  0000 L CNN
F 1 "10u" H 4825 2200 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 4838 2150 50  0001 C CNN
F 3 "" H 4800 2300 50  0000 C CNN
	1    4800 2300
	0    1    1    0   
$EndComp
Wire Wire Line
	5100 2300 5100 2600
Wire Wire Line
	4950 2300 5100 2300
Wire Wire Line
	4500 2300 4650 2300
$Comp
L C C5
U 1 1 5972722E
P 6350 2450
AR Path="/5941B2B4/5972722E" Ref="C5"  Part="1" 
AR Path="/5941F948/5972722E" Ref="C7"  Part="1" 
F 0 "C5" H 6375 2550 50  0000 L CNN
F 1 "10u" H 6375 2350 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 6388 2300 50  0001 C CNN
F 3 "" H 6350 2450 50  0000 C CNN
	1    6350 2450
	-1   0    0    1   
$EndComp
Wire Wire Line
	6200 2300 6350 2300
$Comp
L GND #PWR037
U 1 1 59727314
P 6350 2600
AR Path="/5941B2B4/59727314" Ref="#PWR037"  Part="1" 
AR Path="/5941F948/59727314" Ref="#PWR042"  Part="1" 
F 0 "#PWR037" H 6350 2350 50  0001 C CNN
F 1 "GND" H 6350 2450 50  0000 C CNN
F 2 "" H 6350 2600 50  0000 C CNN
F 3 "" H 6350 2600 50  0000 C CNN
	1    6350 2600
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 597274A4
P 6050 2300
AR Path="/5941B2B4/597274A4" Ref="R3"  Part="1" 
AR Path="/5941F948/597274A4" Ref="R9"  Part="1" 
F 0 "R3" V 6130 2300 50  0000 C CNN
F 1 "10k" V 6050 2300 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 5980 2300 50  0001 C CNN
F 3 "" H 6050 2300 50  0000 C CNN
	1    6050 2300
	0    1    1    0   
$EndComp
Text Label 4500 2300 2    60   ~ 0
3v3f
Text Label 4000 3350 2    60   ~ 0
3v3f
Text Label 5300 3250 2    60   ~ 0
3v3f
Text Label 6600 3150 2    60   ~ 0
3v3f
Text GLabel 6350 2300 2    60   Input ~ 0
ref_filter
Text GLabel 3700 3550 0    60   Input ~ 0
ref_filter
Text GLabel 5000 3450 0    60   Input ~ 0
ref_filter
Text GLabel 6300 3350 0    60   Input ~ 0
ref_filter
$EndSCHEMATC
