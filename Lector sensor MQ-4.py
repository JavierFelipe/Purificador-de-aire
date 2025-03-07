#Sensores MQ-4
from machine import Pin, ADC
import utime
from time import sleep
import math

ledRojo = Pin(26, Pin.OUT)
ledAmarillo = Pin(14, Pin.OUT)
ledVerde = Pin(12, Pin.OUT)


ValorDelSensor = 1

sensor2 = ADC(Pin(33))

ro_mq4 = 67

sensor2.width(ADC.WIDTH_10BIT)
sensor2.atten(ADC.ATTN_11DB)

#Pruebas
a = 1

while a != 100:
    
    a += 1
    
#Lectura de la resistencia Ro para el sensor MQ-4
    
    lectura2 = int(sensor2.read())
    
    ValorDelSensor = ValorDelSensor + lectura2
    ValorDelSensor = ValorDelSensor/100
    Voltaje_rs= (ValorDelSensor)/(1023 * 5)
    rs_aire = 20 *((5/Voltaje_rs - 1))
    ro = rs_aire/4.5
    
    
    print(f"Valor sensor {ValorDelSensor}")
    
    print(f"Volt_sensor {Voltaje_rs}")
    
    print(f"Ro {ro}")
    
    utime.sleep(1)


while True:
    lectura2 = int(sensor2.read())
    Volt_mq4 = (5 * lectura2)/1023
    rs_mq4 = 20 * ((5)/(Volt_mq4 - 1))
    if rs_mq4 != 0:
        ratio_mq4 = rs_mq4/ro_mq4
        m_mq4 = -0.2552
        b_mq4 = 0.1901
        if  ratio_mq4 < 0:
            print("Libre de CH4")
            utime.sleep(1)
        else:
            ppm_log_mq4 = ((math.log10(ratio_mq4)-b_mq4)/(m_mq4))
            ppm_CH4 = math.pow(10, ppm_log_mq4)
            
            print(f"CH4: {ppm_CH4}")
            #utime.sleep(1)
            
            print(ppm_log_mq4)
            
            if ppm_CH4 >= 260:
                ledRojo.on()
                ledAmarillo.off()
                ledVerde.off()
                sleep(2)
                ledRojo.off()
                
            
            elif ppm_CH4 >= 130:
                ledRojo.off()
                ledAmarillo.on()
                sleep(2)
                ledVerde.off()
            
            elif ppm_CH4 < 130 or ppm_CH4 == 0:
                ledRojo.off()
                ledAmarillo.off()
                ledVerde.on()
                sleep(2)
                ledVerde.off()