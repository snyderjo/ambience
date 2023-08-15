---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
title: "Ambience Database"
layout: page
background: "/img/SenseHat.jpg"
---

The idea here is to record ambient state of my residence.

## What's the Impetus? 

As I've aged, the quality of my sleep has deteriorated.  Naturally, I'd like to fix this.  How might I go about doing so?  Collect data.

This page is limited to how I record ambient measures of the room in which I regularly sleep.  My hope is to combine this with the sleep quality data from a wearable to identify any trends.

### The Set Up

I have a [raspberrypi](https://www.raspberrypi.com/) with a [SenseHat](https://www.raspberrypi.com/products/sense-hat/) attachment.   After installing the [sense-hat python package](https://pythonhosted.org/sense-hat/), I created a script which records each of the following
- Temperature
- Pressure
- Humidity
- Orientation
   + pitch
   + roll
   + yaw
- Acceleration
   + pitch
   + roll
   + yaw

This script then runs at an arbirary time interval via [cron](https://en.wikipedia.org/wiki/Cron)--currently set to every five minutes.  Note, I don't expect much variation in orientation or acceleration unless my neighbors are especially amorous or another earthquake hits SLC.

I have also set up a [postgres](https://www.postgresql.org/) database in which to store these data.   This is accomplished through an [Airflow](https://airflow.apache.org/) [DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dags).  Both the postgres database and the Airflow instance are hosted locally on a home server.


### Possible Extensions

Adding a second raspberrypi-sensehat, placing it in my living room to look for any deviations between rooms.  

Comparing the ambient measures in my bedroom against the external weather to estimate my electricity and/or heating bill.
