from datetime import datetime
from dateutil import tz
from sense_hat import SenseHat
import csv

sense = SenseHat()

o = sense.get_orientation()
acceleration = sense.get_accelerometer_raw()

readings = [
    datetime.now(tz = tz.tzlocal())
    ,sense.get_temperature(),sense.get_pressure(),sense.get_humidity()
    ,o["pitch"],o["roll"],o["yaw"]
    ,acceleration["x"],acceleration["y"],acceleration["z"]
    ]

outputfile = "path/to/output/readings_" + datetime.now().strftime("%Y_%m_%d") + ".csv"

with open(outputfile,"a") as f:
    write = csv.writer(f)
    write.writerow(readings)
