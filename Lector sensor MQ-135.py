#Sensores MQ-135
from machine import Pin, ADC
import utime
from time import sleep
import math

ledRojo = Pin(26, Pin.OUT)
ledAmarillo = Pin(14, Pin.OUT)
ledVerde = Pin(12, Pin.OUT)

ro_mq135 = 57

ValorDelSensor = 1

sensor = ADC(Pin(32))

sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)

#Pruebas
a = 1

while a != 100:
    
    a += 1
    
Lectura de la resistencia Ro para el sensor MQ-135
    
    lectura = int(sensor.read())
    
    ValorDelSensor = ValorDelSensor + lectura
    ValorDelSensor = ValorDelSensor/100
    Voltaje_rs= (ValorDelSensor)/(1023 * 5)
    rs_aire = 20 *((5/Voltaje_rs - 1))
    ro = rs_aire/3.8
    
    
    print(f"Valor sensor {ValorDelSensor}")
    
    print(f"Volt_sensor {Voltaje_rs}")
    
    print(f"Ro {ro}")
    
    utime.sleep(1)

while True:
    lectura = int(sensor.read())
    Volt_mq135 = (5 * lectura)/1023
    
    rs_mq135 = 20 * ((5)/(Volt_mq135 - 1))
    if rs_mq135 !=0: 
        ratio_mq135 = rs_mq135/ro_mq135
        m_mq135 = -0.2839
        b_mq135 = 0.6818
        if  ratio_mq135 < 0:
            print("Libre de CO2")
            utime.sleep(1)
        else:    
            ppm_log_mq135 = ((math.log10(ratio_mq135)-b_mq135)/(m_mq135))
            ppm_CO2 = math.pow(10, ppm_log_mq135)
        
            print(f"CO2: {ppm_CO2}")
            utime.sleep(1)
        
            if ppm_CO2 >= 1200:
                ledRojo.on()
                ledAmarillo.off()
                ledVerde.off()
                sleep(3)
                ledRojo.off()
            
            
            elif ppm_CO2 >= 500:
                ledRojo.off()
                ledAmarillo.on()
                ledVerde.off()
            
            elif ppm_CO2 < 500 or ppm_CO2 == 0:
                ledRojo.off()
                ledAmarillo.off()
                ledVerde.on()
                sleep(3)
                ledVerde.off()