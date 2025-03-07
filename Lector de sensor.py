from machine import Pin, ADC
import utime
from time import sleep
import math
from machine import Pin, I2C
import ssd1306
import time

ledRojo = Pin(26, Pin.OUT)
ledAmarillo = Pin(14, Pin.OUT)
ledVerde = Pin(12, Pin.OUT)


ValorDelSensor = 1

sensor = ADC(Pin(32))
sensor2 = ADC(Pin(33))
sensor3 = ADC(Pin(35))

sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)

sensor2.width(ADC.WIDTH_10BIT)
sensor2.atten(ADC.ATTN_11DB)

sensor3.width(ADC.WIDTH_10BIT)
sensor3.atten(ADC.ATTN_11DB)


ro_mq135 = 57

ro_mq4 = 20

a = 1

    
#Lectura de CO2 en el ambiente por el sensor MQ-135    
    
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
                sleep(2)
                ledRojo.off()
                
            
            elif ppm_CO2 >= 500:
                ledRojo.off()
                ledAmarillo.on()
                sleep(2)
                ledVerde.off()
            
            elif ppm_CO2 < 500 or ppm_CO2 == 0:
                ledRojo.off()
                ledAmarillo.off()
                ledVerde.on()
                sleep(2)
                ledVerde.off()
                
#Lectura de CO2 en el ambiente por el segundo sensor MQ-135


    lectura3 = int(sensor3.read())
    Volt_mq135 = (5 * lectura3)/1023
    
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
            

#Lectura de CH4 en el ambiente por el sensor MQ-4   

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
            
#Lectura de CH4 en el ambiente por el segundo sensor MQ-4
                
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
            
#Pantalla OLED
            
            i2c = I2C(0, scl = Pin(22), sda = Pin(21))

            oled_width = 128
            oled_height = 64
            oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

            oled.text(f"CO2: {ppm_CO2}", 10, 10)
            oled.show()
            time.sleep(2)
            oled.text(f"CH4: {ppm_CH4}", 10, 25)
            time.sleep(2)
            oled.show()

#Configuración del ventilador 

# Configurar el GPIO como salida PWM (ejemplo: GPIO 5)
fan = PWM(Pin(5))  
fan.freq(25000)  # Aumentar la frecuencia a 25 kHz para evitar ruido

def set_speed(duty):
    """Controla la velocidad del ventilador (0-1023)"""
    fan.duty(duty)

# Sobrecarga inicial solo una vez al inicio
print("Sobrecarga inicial (100%)")
set_speed(1023)  # Máxima velocidad para asegurar arranque
sleep(1)         # Espera 1 segundo para arrancar bien

# Mantener velocidad constante (ajústala según necesidad)
velocidad_deseada = 850  # Ajusta entre 0 y 1023
print(f"Manteniendo velocidad al {velocidad_deseada}/1023")
set_speed(velocidad_deseada)

# Mantener el código corriendo sin hacer nada más
while True:
    sleep(1)  # Evita que el script termine

            

        
   
        
        
        
    
    
            
    
    
        

    

    


    
        
        
    