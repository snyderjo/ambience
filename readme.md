## Ambiance Data

This repository contains the code to record ambient data from a [raspberry pi](https://www.raspberrypi.com/) with a [sense hat](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat) attahcment and store it in a postgresql database.

The three directories contain code specific to:  
* raspberry-pi-specific code (sensehat_cron_scripts)
* creation of the necessary SQL tables (SQL_tables)
* Directed Acyclic Graphs (dags) that can be run on a local instance of airflow to pull data from the raspberry pi into the SQL database.

Currently, the data recorded are:
* temperature;
* pressure;
* humidity;
* magnomometer readings of:
    + pitch,
    + roll, and
    + yaw; and
* accelerometer readings of:
    + side-to-side
    + back-and-forth
    + up-and-down.

I expect there to be little in the way of variation in the last six measures unless we have another earthquake, my neighbors are especially amorous, or earth's magnetic poles unexpectedly switch.

One can specify the cadence of recordings in any cron-job as specified on the raspberry pi.  I currently have mine set to every five minutes.