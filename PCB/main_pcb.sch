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
Sheet 1 3
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
L Teensy_3.1 U1
U 1 1 59417824
P 2950 4450
F 0 "U1" H 2950 5200 60  0000 C CNN
F 1 "Teensy_3.1" H 3000 5650 60  0000 C CNN
F 2 "Teensy-3.1:Teensy-3.1" H 3050 4450 60  0001 C CNN
F 3 "" H 3050 4450 60  0000 C CNN
	1    2950 4450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 594178CB
P 1300 3150
F 0 "#PWR01" H 1300 2900 50  0001 C CNN
F 1 "GND" H 1300 3000 50  0000 C CNN
F 2 "" H 1300 3150 50  0000 C CNN
F 3 "" H 1300 3150 50  0000 C CNN
	1    1300 3150
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR02
U 1 1 59417961
P 4250 3450
F 0 "#PWR02" H 4250 3300 50  0001 C CNN
F 1 "+3V3" H 4250 3590 50  0000 C CNN
F 2 "" H 4250 3450 50  0000 C CNN
F 3 "" H 4250 3450 50  0000 C CNN
	1    4250 3450
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR03
U 1 1 59417D8E
P 3400 1800
F 0 "#PWR03" H 3400 1650 50  0001 C CNN
F 1 "+3V3" H 3400 1940 50  0000 C CNN
F 2 "" H 3400 1800 50  0000 C CNN
F 3 "" H 3400 1800 50  0000 C CNN
	1    3400 1800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 59417DA5
P 3400 2400
F 0 "#PWR04" H 3400 2150 50  0001 C CNN
F 1 "GND" H 3400 2250 50  0000 C CNN
F 2 "" H 3400 2400 50  0000 C CNN
F 3 "" H 3400 2400 50  0000 C CNN
	1    3400 2400
	1    0    0    -1  
$EndComp
$Comp
L R Rd2
U 1 1 59417DC6
P 3400 2250
F 0 "Rd2" V 3480 2250 50  0000 C CNN
F 1 "1.5k" V 3400 2250 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 3330 2250 50  0001 C CNN
F 3 "" H 3400 2250 50  0000 C CNN
	1    3400 2250
	1    0    0    -1  
$EndComp
$Comp
L R Rd1
U 1 1 59417F1F
P 3400 1950
F 0 "Rd1" V 3480 1950 50  0000 C CNN
F 1 "6.2k" V 3400 1950 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 3330 1950 50  0001 C CNN
F 3 "" H 3400 1950 50  0000 C CNN
	1    3400 1950
	1    0    0    -1  
$EndComp
Text Label 3550 2100 0    60   ~ 0
Vref
$Comp
L CONN_01X03 P1
U 1 1 594185AC
P 4300 2350
F 0 "P1" H 4300 2550 50  0000 C CNN
F 1 "SEN" V 4400 2350 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 4300 2350 50  0001 C CNN
F 3 "" H 4300 2350 50  0000 C CNN
	1    4300 2350
	0    1    1    0   
$EndComp
$Comp
L GND #PWR05
U 1 1 5941862F
P 4600 2150
F 0 "#PWR05" H 4600 1900 50  0001 C CNN
F 1 "GND" H 4600 2000 50  0000 C CNN
F 2 "" H 4600 2150 50  0000 C CNN
F 3 "" H 4600 2150 50  0000 C CNN
	1    4600 2150
	1    0    0    -1  
$EndComp
Text Label 4300 2150 1    60   ~ 0
Sen1
Text Label 4200 2150 1    60   ~ 0
Sen2
Text Label 4050 4650 0    60   ~ 0
FFT1
$Comp
L CONN_01X03 P2
U 1 1 5941A6DB
P 5150 2350
F 0 "P2" H 5150 2550 50  0000 C CNN
F 1 "SRV" V 5250 2350 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 5150 2350 50  0001 C CNN
F 3 "" H 5150 2350 50  0000 C CNN
	1    5150 2350
	0    1    1    0   
$EndComp
$Comp
L GND #PWR06
U 1 1 5941A83B
P 5500 2150
F 0 "#PWR06" H 5500 1900 50  0001 C CNN
F 1 "GND" H 5500 2000 50  0000 C CNN
F 2 "" H 5500 2150 50  0000 C CNN
F 3 "" H 5500 2150 50  0000 C CNN
	1    5500 2150
	1    0    0    -1  
$EndComp
$Comp
L VDD #PWR07
U 1 1 5941A89E
P 4100 3150
F 0 "#PWR07" H 4100 3000 50  0001 C CNN
F 1 "VDD" H 4100 3300 50  0000 C CNN
F 2 "" H 4100 3150 50  0000 C CNN
F 3 "" H 4100 3150 50  0000 C CNN
	1    4100 3150
	1    0    0    -1  
$EndComp
$Comp
L VDD #PWR08
U 1 1 5941A916
P 5150 2150
F 0 "#PWR08" H 5150 2000 50  0001 C CNN
F 1 "VDD" H 5150 2300 50  0000 C CNN
F 2 "" H 5150 2150 50  0000 C CNN
F 3 "" H 5150 2150 50  0000 C CNN
	1    5150 2150
	1    0    0    -1  
$EndComp
Text Label 1850 3750 2    60   ~ 0
SRV
Text Label 4950 2150 2    60   ~ 0
SRV
$Sheet
S 5900 3000 650  550 
U 5941B2B4
F0 "AnalogFilter1" 60
F1 "analogFilter.sch" 60
F2 "Vcc" I L 5900 3100 60 
F3 "GND" I L 5900 3200 60 
F4 "Vref" I L 5900 3300 60 
F5 "Sen" I L 5900 3400 60 
F6 "Out" I R 6550 3250 60 
$EndSheet
$Sheet
S 5900 3850 650  550 
U 5941F948
F0 "AnalogFilter2" 60
F1 "analogFilter.sch" 60
F2 "Vcc" I L 5900 3950 60 
F3 "GND" I L 5900 4050 60 
F4 "Vref" I L 5900 4150 60 
F5 "Sen" I L 5900 4250 60 
F6 "Out" I R 6550 4100 60 
$EndSheet
Text Label 4050 4500 0    60   ~ 0
FFT2
Text Label 6650 3250 0    60   ~ 0
FFT1
Text Label 6650 4100 0    60   ~ 0
FFT2
$Comp
L +3V3 #PWR09
U 1 1 5942025E
P 5750 3100
F 0 "#PWR09" H 5750 2950 50  0001 C CNN
F 1 "+3V3" H 5750 3240 50  0000 C CNN
F 2 "" H 5750 3100 50  0000 C CNN
F 3 "" H 5750 3100 50  0000 C CNN
	1    5750 3100
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR010
U 1 1 594202E5
P 5750 3950
F 0 "#PWR010" H 5750 3800 50  0001 C CNN
F 1 "+3V3" H 5750 4090 50  0000 C CNN
F 2 "" H 5750 3950 50  0000 C CNN
F 3 "" H 5750 3950 50  0000 C CNN
	1    5750 3950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR011
U 1 1 5942036D
P 5350 3200
F 0 "#PWR011" H 5350 2950 50  0001 C CNN
F 1 "GND" H 5350 3050 50  0000 C CNN
F 2 "" H 5350 3200 50  0000 C CNN
F 3 "" H 5350 3200 50  0000 C CNN
	1    5350 3200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 594203F6
P 5350 4050
F 0 "#PWR012" H 5350 3800 50  0001 C CNN
F 1 "GND" H 5350 3900 50  0000 C CNN
F 2 "" H 5350 4050 50  0000 C CNN
F 3 "" H 5350 4050 50  0000 C CNN
	1    5350 4050
	1    0    0    -1  
$EndComp
Text Label 5800 4150 2    60   ~ 0
Vref
Text Label 5800 3300 2    60   ~ 0
Vref
Text Label 5800 3400 2    60   ~ 0
Sen1
Text Label 5800 4250 2    60   ~ 0
Sen2
$Comp
L RFM69_Breakout U2
U 1 1 59421E75
P 6550 5650
F 0 "U2" H 6550 5600 60  0000 C CNN
F 1 "RFM69_Breakout" H 6550 6600 60  0000 C CNN
F 2 "custom_footprints:RFM69Breakout" H 6550 5650 60  0001 C CNN
F 3 "" H 6550 5650 60  0000 C CNN
	1    6550 5650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 59421F38
P 7400 5550
F 0 "#PWR013" H 7400 5300 50  0001 C CNN
F 1 "GND" H 7400 5400 50  0000 C CNN
F 2 "" H 7400 5550 50  0000 C CNN
F 3 "" H 7400 5550 50  0000 C CNN
	1    7400 5550
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR014
U 1 1 59421FA3
P 5550 5550
F 0 "#PWR014" H 5550 5400 50  0001 C CNN
F 1 "+3V3" H 5550 5690 50  0000 C CNN
F 2 "" H 5550 5550 50  0000 C CNN
F 3 "" H 5550 5550 50  0000 C CNN
	1    5550 5550
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P3
U 1 1 5942423C
P 6600 2200
F 0 "P3" H 6600 2350 50  0000 C CNN
F 1 "PWR" V 6700 2200 50  0000 C CNN
F 2 "Terminal_Blocks:TerminalBlock_Pheonix_MPT-2.54mm_2pol" H 6600 2200 50  0001 C CNN
F 3 "" H 6600 2200 50  0000 C CNN
	1    6600 2200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 594247D7
P 6400 2250
F 0 "#PWR015" H 6400 2000 50  0001 C CNN
F 1 "GND" H 6400 2100 50  0000 C CNN
F 2 "" H 6400 2250 50  0000 C CNN
F 3 "" H 6400 2250 50  0000 C CNN
	1    6400 2250
	1    0    0    -1  
$EndComp
$Comp
L VDD #PWR016
U 1 1 59424AF2
P 6400 2150
F 0 "#PWR016" H 6400 2000 50  0001 C CNN
F 1 "VDD" H 6400 2300 50  0000 C CNN
F 2 "" H 6400 2150 50  0000 C CNN
F 3 "" H 6400 2150 50  0000 C CNN
	1    6400 2150
	1    0    0    -1  
$EndComp
Text Label 5700 4850 2    60   ~ 0
MISO
Text Label 5700 4950 2    60   ~ 0
MOSI
Text Label 5700 5050 2    60   ~ 0
SCK
Text Label 5700 5150 2    60   ~ 0
RadCS
Text Label 5700 5350 2    60   ~ 0
RadInt
Text Label 1850 5100 2    60   ~ 0
MISO
Text Label 1850 4950 2    60   ~ 0
MOSI
Text Label 1850 4800 2    60   ~ 0
RadCS
Text Label 4050 5100 0    60   ~ 0
SCK
Text Label 1850 3300 2    60   ~ 0
RadInt
Text Label 1850 4200 2    60   ~ 0
LED
$Comp
L Q_NMOS_SDG Q1
U 1 1 5942A854
P 7400 2550
F 0 "Q1" H 7700 2600 50  0000 R CNN
F 1 "5LN01SP" H 7950 2500 50  0000 R CNN
F 2 "TO_SOT_Packages_THT:TO-92_Inline_Wide" H 7600 2650 50  0001 C CNN
F 3 "" H 7400 2550 50  0000 C CNN
	1    7400 2550
	1    0    0    -1  
$EndComp
$Comp
L R R13
U 1 1 5942A989
P 7500 1800
F 0 "R13" V 7580 1800 50  0000 C CNN
F 1 "10R" V 7500 1800 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 7430 1800 50  0001 C CNN
F 3 "" H 7500 1800 50  0000 C CNN
	1    7500 1800
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P4
U 1 1 5942BAC8
P 7700 2150
F 0 "P4" H 7700 2300 50  0000 C CNN
F 1 "LED" V 7800 2150 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x01_Pitch2.54mm" H 7700 2150 50  0001 C CNN
F 3 "" H 7700 2150 50  0000 C CNN
	1    7700 2150
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR017
U 1 1 5942BEAF
P 7500 1650
F 0 "#PWR017" H 7500 1500 50  0001 C CNN
F 1 "+3V3" H 7500 1790 50  0000 C CNN
F 2 "" H 7500 1650 50  0000 C CNN
F 3 "" H 7500 1650 50  0000 C CNN
	1    7500 1650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR018
U 1 1 5942BF14
P 7500 2750
F 0 "#PWR018" H 7500 2500 50  0001 C CNN
F 1 "GND" H 7500 2600 50  0000 C CNN
F 2 "" H 7500 2750 50  0000 C CNN
F 3 "" H 7500 2750 50  0000 C CNN
	1    7500 2750
	1    0    0    -1  
$EndComp
Text Label 7200 2550 2    60   ~ 0
LED
$Comp
L VDD #PWR019
U 1 1 5942D4E4
P 9150 3250
F 0 "#PWR019" H 9150 3100 50  0001 C CNN
F 1 "VDD" H 9150 3400 50  0000 C CNN
F 2 "" H 9150 3250 50  0000 C CNN
F 3 "" H 9150 3250 50  0000 C CNN
	1    9150 3250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR020
U 1 1 5942D5BE
P 9850 3350
F 0 "#PWR020" H 9850 3100 50  0001 C CNN
F 1 "GND" H 9850 3200 50  0000 C CNN
F 2 "" H 9850 3350 50  0000 C CNN
F 3 "" H 9850 3350 50  0000 C CNN
	1    9850 3350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR021
U 1 1 5942D66E
P 9150 3950
F 0 "#PWR021" H 9150 3700 50  0001 C CNN
F 1 "GND" H 9150 3800 50  0000 C CNN
F 2 "" H 9150 3950 50  0000 C CNN
F 3 "" H 9150 3950 50  0000 C CNN
	1    9150 3950
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR022
U 1 1 5942D81E
P 7850 3750
F 0 "#PWR022" H 7850 3600 50  0001 C CNN
F 1 "+3V3" H 7850 3890 50  0000 C CNN
F 2 "" H 7850 3750 50  0000 C CNN
F 3 "" H 7850 3750 50  0000 C CNN
	1    7850 3750
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P5
U 1 1 5942DE0F
P 9350 3600
F 0 "P5" H 9350 3850 50  0000 C CNN
F 1 "M1" V 9450 3600 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x04_Pitch2.54mm" H 9350 3600 50  0001 C CNN
F 3 "" H 9350 3600 50  0000 C CNN
	1    9350 3600
	1    0    0    -1  
$EndComp
Text Label 4050 3600 0    60   ~ 0
STEP1
Text Label 4050 3750 0    60   ~ 0
STEP2
Text Label 4050 3900 0    60   ~ 0
DIR1
Text Label 4050 4050 0    60   ~ 0
DIR2
Text Label 8050 3850 2    60   ~ 0
STEP1
Text Label 8050 3950 2    60   ~ 0
DIR1
$Comp
L VDD #PWR023
U 1 1 5943137C
P 9600 4650
F 0 "#PWR023" H 9600 4500 50  0001 C CNN
F 1 "VDD" H 9600 4800 50  0000 C CNN
F 2 "" H 9600 4650 50  0000 C CNN
F 3 "" H 9600 4650 50  0000 C CNN
	1    9600 4650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR024
U 1 1 59431382
P 10300 4650
F 0 "#PWR024" H 10300 4400 50  0001 C CNN
F 1 "GND" H 10300 4500 50  0000 C CNN
F 2 "" H 10300 4650 50  0000 C CNN
F 3 "" H 10300 4650 50  0000 C CNN
	1    10300 4650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR025
U 1 1 59431388
P 9600 5350
F 0 "#PWR025" H 9600 5100 50  0001 C CNN
F 1 "GND" H 9600 5200 50  0000 C CNN
F 2 "" H 9600 5350 50  0000 C CNN
F 3 "" H 9600 5350 50  0000 C CNN
	1    9600 5350
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR026
U 1 1 5943138E
P 8300 5150
F 0 "#PWR026" H 8300 5000 50  0001 C CNN
F 1 "+3V3" H 8300 5290 50  0000 C CNN
F 2 "" H 8300 5150 50  0000 C CNN
F 3 "" H 8300 5150 50  0000 C CNN
	1    8300 5150
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P6
U 1 1 59431395
P 9800 5000
F 0 "P6" H 9800 5250 50  0000 C CNN
F 1 "M2" V 9900 5000 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x04_Pitch2.54mm" H 9800 5000 50  0001 C CNN
F 3 "" H 9800 5000 50  0000 C CNN
	1    9800 5000
	1    0    0    -1  
$EndComp
Text Label 8500 5250 2    60   ~ 0
STEP2
Text Label 8500 5350 2    60   ~ 0
DIR2
$Comp
L CP1 C3
U 1 1 5943377D
P 6050 2200
F 0 "C3" H 5850 2300 50  0000 L CNN
F 1 "470uF" H 5800 2100 50  0000 L CNN
F 2 "Capacitors_ThroughHole:CP_Radial_D10.0mm_P5.00mm" H 6050 2200 50  0001 C CNN
F 3 "" H 6050 2200 50  0000 C CNN
	1    6050 2200
	1    0    0    -1  
$EndComp
$Comp
L DRV8834_Breakout U5
U 1 1 59430826
P 8600 4050
F 0 "U5" H 8600 4000 60  0000 C CNN
F 1 "DRV8834_Breakout" H 8600 5000 60  0000 C CNN
F 2 "custom_footprints:DRV8834Breakout" H 8600 4050 60  0001 C CNN
F 3 "" H 8600 4050 60  0000 C CNN
	1    8600 4050
	1    0    0    -1  
$EndComp
$Comp
L DRV8834_Breakout U6
U 1 1 59430923
P 9050 5450
F 0 "U6" H 9050 5400 60  0000 C CNN
F 1 "DRV8834_Breakout" H 9050 6400 60  0000 C CNN
F 2 "custom_footprints:DRV8834Breakout" H 9050 5450 60  0001 C CNN
F 3 "" H 9050 5450 60  0000 C CNN
	1    9050 5450
	1    0    0    -1  
$EndComp
$Comp
L CONN_02X03 P7
U 1 1 59495D5E
P 7550 3400
F 0 "P7" H 7550 3600 50  0000 C CNN
F 1 "CONN_02X03" H 7550 3200 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm" H 7550 2200 50  0001 C CNN
F 3 "" H 7550 2200 50  0000 C CNN
	1    7550 3400
	0    1    1    0   
$EndComp
Wire Wire Line
	3400 2100 3550 2100
Wire Wire Line
	4400 2150 4600 2150
Wire Wire Line
	4050 4650 3950 4650
Wire Wire Line
	5250 2150 5500 2150
Wire Wire Line
	4100 3150 3950 3150
Wire Wire Line
	1950 3750 1850 3750
Wire Wire Line
	4950 2150 5050 2150
Wire Wire Line
	4050 4500 3950 4500
Wire Wire Line
	6650 3250 6550 3250
Wire Wire Line
	6650 4100 6550 4100
Wire Wire Line
	5750 3100 5900 3100
Wire Wire Line
	5750 3950 5900 3950
Wire Wire Line
	5350 3200 5900 3200
Wire Wire Line
	5350 4050 5900 4050
Wire Wire Line
	5800 4150 5900 4150
Wire Wire Line
	5800 3300 5900 3300
Wire Wire Line
	5800 3400 5900 3400
Wire Wire Line
	5800 4250 5900 4250
Wire Wire Line
	5550 5550 5700 5550
Wire Wire Line
	1850 5100 1950 5100
Wire Wire Line
	1850 4950 1950 4950
Wire Wire Line
	1850 4800 1950 4800
Wire Wire Line
	4050 5100 3950 5100
Wire Wire Line
	1850 3300 1950 3300
Wire Wire Line
	1850 4200 1950 4200
Wire Wire Line
	7500 1950 7500 2100
Wire Wire Line
	7500 2200 7500 2350
Wire Wire Line
	7850 3750 8050 3750
Wire Wire Line
	9150 3350 9250 3350
Wire Wire Line
	9250 3350 9250 3250
Wire Wire Line
	9250 3250 9850 3250
Wire Wire Line
	9850 3250 9850 3350
Wire Wire Line
	3950 3600 4050 3600
Wire Wire Line
	4050 3750 3950 3750
Wire Wire Line
	3950 3900 4050 3900
Wire Wire Line
	4050 4050 3950 4050
Wire Wire Line
	8300 5150 8500 5150
Wire Wire Line
	9600 4750 9700 4750
Wire Wire Line
	9700 4750 9700 4650
Wire Wire Line
	9700 4650 10300 4650
Wire Wire Line
	6400 2150 6250 2150
Wire Wire Line
	6250 2150 6250 1950
Wire Wire Line
	6250 1950 6050 1950
Wire Wire Line
	6050 1950 6050 2050
Wire Wire Line
	6050 2350 6050 2400
Wire Wire Line
	6050 2400 6250 2400
Wire Wire Line
	6250 2400 6250 2250
Wire Wire Line
	6250 2250 6400 2250
Wire Wire Line
	1300 3150 1950 3150
Wire Wire Line
	4250 3450 3950 3450
Wire Wire Line
	7550 3150 7550 3050
Wire Wire Line
	7550 3050 7900 3050
Wire Wire Line
	7900 3050 7900 3350
Wire Wire Line
	7900 3350 8050 3350
Wire Wire Line
	7550 3650 7550 3700
Wire Wire Line
	7550 3700 7750 3700
Wire Wire Line
	7750 3700 7750 3450
Wire Wire Line
	7750 3450 8050 3450
Wire Wire Line
	7450 3150 7450 3650
Wire Wire Line
	7650 3150 7650 3800
$Comp
L +3V3 #PWR027
U 1 1 59496101
P 7450 3150
F 0 "#PWR027" H 7450 3000 50  0001 C CNN
F 1 "+3V3" H 7450 3290 50  0000 C CNN
F 2 "" H 7450 3150 50  0000 C CNN
F 3 "" H 7450 3150 50  0000 C CNN
	1    7450 3150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR028
U 1 1 59496178
P 7650 3800
F 0 "#PWR028" H 7650 3550 50  0001 C CNN
F 1 "GND" H 7650 3650 50  0000 C CNN
F 2 "" H 7650 3800 50  0000 C CNN
F 3 "" H 7650 3800 50  0000 C CNN
	1    7650 3800
	1    0    0    -1  
$EndComp
Connection ~ 7650 3650
$Comp
L CONN_02X03 P8
U 1 1 594962DC
P 8000 4800
F 0 "P8" H 8000 5000 50  0000 C CNN
F 1 "CONN_02X03" H 8000 4600 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm" H 8000 3600 50  0001 C CNN
F 3 "" H 8000 3600 50  0000 C CNN
	1    8000 4800
	0    1    1    0   
$EndComp
Wire Wire Line
	8000 4550 8000 4450
Wire Wire Line
	8000 4450 8350 4450
Wire Wire Line
	8000 5050 8000 5100
Wire Wire Line
	8000 5100 8200 5100
Wire Wire Line
	8200 5100 8200 4850
Wire Wire Line
	8200 4850 8500 4850
Wire Wire Line
	8100 4550 8100 5200
$Comp
L +3V3 #PWR029
U 1 1 594962EA
P 7900 4550
F 0 "#PWR029" H 7900 4400 50  0001 C CNN
F 1 "+3V3" H 7900 4690 50  0000 C CNN
F 2 "" H 7900 4550 50  0000 C CNN
F 3 "" H 7900 4550 50  0000 C CNN
	1    7900 4550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR030
U 1 1 594962F0
P 8100 5200
F 0 "#PWR030" H 8100 4950 50  0001 C CNN
F 1 "GND" H 8100 5050 50  0000 C CNN
F 2 "" H 8100 5200 50  0000 C CNN
F 3 "" H 8100 5200 50  0000 C CNN
	1    8100 5200
	1    0    0    -1  
$EndComp
Connection ~ 8100 5050
Wire Wire Line
	8350 4450 8350 4750
Wire Wire Line
	8350 4750 8500 4750
Wire Wire Line
	7900 4550 7900 5050
$Comp
L +3V3 #PWR031
U 1 1 59496C29
P 2950 6100
F 0 "#PWR031" H 2950 5950 50  0001 C CNN
F 1 "+3V3" H 2950 6240 50  0000 C CNN
F 2 "" H 2950 6100 50  0000 C CNN
F 3 "" H 2950 6100 50  0000 C CNN
	1    2950 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 6100 2850 6100
Wire Wire Line
	2850 6100 2850 5650
$Comp
L GND #PWR032
U 1 1 594A8840
P 7550 5350
F 0 "#PWR032" H 7550 5100 50  0001 C CNN
F 1 "GND" H 7550 5200 50  0000 C CNN
F 2 "" H 7550 5350 50  0000 C CNN
F 3 "" H 7550 5350 50  0000 C CNN
	1    7550 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 5350 7550 5350
$EndSCHEMATC
