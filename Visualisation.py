import serial
import re
import matplotlib.pyplot as plt
import time
import sys

import json

# Serielle Verbindung herstellen
ser = serial.Serial('/dev/cu.usbserial-1440', 115200)


# Datenpuffer initialisieren
data_buffer = ''

 

# Plot-Daten initialisieren
temperature = []
humidity = []
acceleration_x = []
acceleration_y = []
acceleration_z = []
gyro_x = []
gyro_y = []
gyro_z = []
damper_fr = []
damper_fh = []
timestamps = [] # Eine Liste, um die Zeitstempel der Daten zu speichern

 

# Plot-Fenster initialisieren
plt.ion()
fig, axes = plt.subplots(3, 2, figsize=(12, 8))

 

# Startzeit festlegen
start_time = time.time()

round_counter = 0

# Haupt-Loop
while True:

    # Daten über UART lesen
    data = ser.readline().decode('utf-8').strip()

    #serial.Serial.flush(ser)
 

    print("gelesene Daten:",data)
    daten_liste = []
 

    if data:
        # Daten analysieren und extrahieren
        zeit = time.time()

        daten = json.loads(data)

        temperatur = daten['temp']


        match = re.search(r'temp:([-+]?[0-9]*\.?[0-9]+)°C', data)
        if match:
            temperature.append(float(match.group(1)))
            timestamps.append(time.time() - start_time)

 

        match = re.search(r'humm:([-+]?[0-9]*\.?[0-9]+)%', data)
        if match:
            humidity.append(float(match.group(1)))


        match = re.search(r'acc_x:([-+]?[0-9]+)mg', data)
        if match:
            acceleration_x.append(int(match.group(1)))

    

        match = re.search(r'acc_y:([-+]?[0-9]+)mg', data)
        if match:
            acceleration_y.append(int(match.group(1)))

    

        match = re.search(r'acc_z:([-+]?[0-9]+)mg', data)
        if match:
            acceleration_z.append(int(match.group(1)))

    

        match = re.search(r'gyro_X:([-+]?[0-9]+)mdps', data)
        if match:
            gyro_x.append(int(match.group(1)))

    

        match = re.search(r'gyro_Y:([-+]?[0-9]+)mdps', data)
        if match:
            gyro_y.append(int(match.group(1)))

    

        match = re.search(r'gyro_Z:([-+]?[0-9]+)mdps', data)
        if match:
            gyro_z.append(int(match.group(1)))

    

        match = re.search(r'damper_fr:([-+]?[0-9]*\.?[0-9]+)V', data)
        if match:
            damper_fr.append(float(match.group(1)))

    

        match = re.search(r'damper_fh:([-+]?[0-9]*\.?[0-9]+)V', data)
        if match:
            damper_fh.append(float(match.group(1)))

        print("match Zeit: " ,time.time() - zeit)

      

    
        zeit = time.time()
        # Ältere Daten entfernen

        timestamps = timestamps[-50:]
        temperature = temperature[-50:]
        # ...

        while timestamps and timestamps[0] < time.time() - start_time - 5:
            timestamps.pop(0)
            temperature.pop(0)
            humidity.pop(0)
            acceleration_x.pop(0)
            acceleration_y.pop(0)
            acceleration_z.pop(0)
            gyro_x.pop(0)
            gyro_y.pop(0)
            gyro_z.pop(0)
            damper_fh.pop(0)
            damper_fr.pop(0)
            
        print("timestamps Zeit: " ,time.time() - zeit)
 

        data = ""

 
    #if(round_counter)
        
        # Plots aktualisieren

        # current_time = time.time()
        # axes[0, 0].clear()
        # axes[0, 0].plot([t-current_time for t in timestamps], temperature, 'r')
        # axes[0, 0].set_title('Temperature')
        # axes[0, 0].set_xlim([-10, 0]) # Set x limits to -10 and 0.

        

        # axes[0, 1].clear()
        # axes[0, 1].plot(humidity, 'g')
        # axes[0, 1].set_title('Humidity')

        

        axes[1, 0].clear()
        axes[1, 0].plot(acceleration_x, 'b')
        axes[1, 0].set_title('Acceleration X')

        

        axes[1, 1].clear()
        axes[1, 1].plot(acceleration_y, 'm')
        axes[1, 1].set_title('Acceleration Y')

        

        axes[2, 0].clear()
        axes[2, 0].plot(acceleration_z, 'c')
        axes[2, 0].set_title('Acceleration Z')

        

        # axes[2, 1].clear()
        # axes[2, 1].plot(gyro_x, 'y')
        # axes[2, 1].set_title('Gyro X')

        
        zeit = time.time()
        axes[0, 0].clear()
        axes[0, 0].plot(damper_fr, 'g')
        axes[0, 0].set_title('Damper FR')
        print("Plot Zeit: " ,time.time() - zeit)

        

        axes[0, 1].clear()
        axes[0, 1].plot(damper_fh, 'b')
        axes[0, 1].set_title('Damper FH')

        

        # axes[1, 0].clear()
        # axes[1, 0].plot(gyro_y, 'r')
        # axes[1, 0].set_title('Gyro Y')



        # axes[1, 1].clear()
        # axes[1, 1].plot(gyro_z, 'm')
        # axes[1, 1].set_title('Gyro Z')

    

        # Plot-Layout anpassen
        plt.tight_layout()
        
        
        
        # Plots anzeigen
        plt.draw()
        plt.pause(0)
    
    
       

 

# Serielle Verbindung schließen
ser.close()
plt.show(block=True)