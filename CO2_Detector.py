import board
import adafruit_scd4x
from adafruit_extended_bus import ExtendedI2C as I2C
import time, os
import datetime

#create file name in the form:  Data From DD-MM-YY, Start Time HH-MM-SS.txt
file_name=f"Data From {datetime.date.today().strftime('%d-%m-%y')}, Start Time {datetime.datetime.now().strftime('%H-%M-%S')}.txt"
file_location = os.path.join("/home/Jim/env", file_name)

#create file if not exists
try:
	records = open(file_location, "r")
except:
	records = open(file_location, "w")
records.close()
print('file created successfully...')

#set up board
i2c = I2C(1)
scd4x = adafruit_scd4x.SCD4X(i2c)
print('board setup complete...')

#start measurements
scd4x.start_periodic_measurement()
print("waiting for first measurement...")

minutes_between_samples=0.5
while True:
	if scd4x.data_ready:
		data = open(file_location, "a")
		#read sensor data
		ppm=scd4x.CO2
		temp=scd4x.temperature
		humidity=scd4x.relative_humidity
		#create timestamp in the from HH:MM:SS/DD-MM-YYYY
		timestamp=f"{datetime.datetime.now().strftime('%H:%M:%S')}/{datetime.date.today().strftime('%d-%m-%Y')}"
		#print data to terminal
		print(f"CO2: {ppm} ppm")
		print(f"Temperature: {temp:.2f}*C")
		print(f"Humidiy: {humidity:.2f} %")
		print(f"Time: {timestamp}\n")
		#write data to file
		data.write(f"{timestamp},{ppm},{temp:.2f},{humidity:.2f}\n")
		data.close()
		#wait until next sample
		time.sleep(60 * minutes_between_samples)
