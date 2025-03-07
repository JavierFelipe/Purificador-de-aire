#Configuración del ventilador 

Configurar el GPIO como salida PWM (ejemplo: GPIO 5)
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