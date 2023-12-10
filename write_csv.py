import serial
import csv

# Set the serial port and baud rate to match your Arduino
ser = serial.Serial('COM5', 9600)  # Replace 'COM4' with your Arduino's serial port

# Open a CSV file for writing
with open('fsr_data2.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the header row if needed
    csv_writer.writerow(["Readings (ohms)"])

    try:
        while True:
            # Read a line of data from the Arduino
            data = ser.readline().decode().strip()
            if data:
                reading = data
                csv_writer.writerow([reading])
    except KeyboardInterrupt:
        # Close the serial port
        ser.close()

