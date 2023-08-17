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
- Temperature (in Celcius)
- Pressure (in Millibars)
- Humidity (percentage)
- Orientation (in degrees)
   + pitch 
   + roll
   + yaw
- Acceleration (in G's)
   + pitch
   + roll
   + yaw  

to a dated csv stored on the pi.  This script then runs at an arbirary time interval via [cron](https://en.wikipedia.org/wiki/Cron)--currently set to every five minutes.  Note, unless my neighbors are especially amorous or [another earthquake hits SLC](https://en.wikipedia.org/wiki/2020_Salt_Lake_City_earthquake), I don't expect much variation in orientation or acceleration.

I have also set up a [postgres](https://www.postgresql.org/) database and schema in which to store these data.   This is accomplished through an [Airflow](https://airflow.apache.org/) [DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dags) on a daily basis.  Both the postgres database and the Airflow instance are hosted locally on a home server.

### Possible Extensions

Adding a second raspberrypi-sensehat, placing it in my living room to look for any deviations between rooms.  

Comparing the ambient measures in my bedroom against the external weather to estimate my electricity and/or heating bill.


# Tools Applied / Learned 

<table style="padding:30px;font-size:17px;">

<br>

<tr>
    <td align="center">
        <div>
            <a href="https://airflow.apache.org/" target="_blank"><img src="img/icons/airflow_transparent.png" alt="1" height="140px" width="140px"></a>
        </div>
    </td>
    <td  align="center">
        <div>
            <a href="https://www.postgresql.org/" target="_blank"><img src="img/icons/PostgreSQL_logo.3colors.svg" alt="2" height="140px" width="140px"></a>
        </div>
    </td>
    <td  align="center">
        <div>
            <a href="https://www.raspberrypi.com/" target="_blank"><img src="img/icons/Raspberry_Pi-Logo.wine.svg" alt="3" height="140px" width="140px"></a>
        </div>
    </td>
</tr>
<tr>
    <td>
        <div>
            <p style="text-align:center">Airflow is a remarkably robust scheduling tool, commonly used in ETL processes.  Here, I use it to pull data recorded on and by the pi to the database.</p>
        </div>
    </td>
    <td >
        <div>
            <p style="text-align:center">Postgres is a free and open-source Relational Database Management System--a flavor of SQL database.  It is the distribution I used to store the data.</p>
        </div>
    </td>
    <td >
        <div>
            <p style="text-align:center">RaspberryPi's are remarkable!  They have any number of <a href="https://projects.raspberrypi.org/en/projects" target="_blank">applications and potential projects</a>.</p>
        </div>
    </td>
</tr>
</table>

<br>
