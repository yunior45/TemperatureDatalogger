# TemperatureDatalogger

-- CEN4216 Cyberphysical systems Project --

The temperature datalogger application is intended to take temperature readings
at the FGCU BioGas experimental plant and store the data in an AWS DynamoDB 
database table to later be used by the VR lab. This project has two parts, 
first the 'TempSensing' is on the actual datalogger installed at the plant and
is taking temperature reading in intervals predetermined by the user. The 'ConsoleSensing'
file is for demoing purposes to show how the data would be pulled from the table
to an interface.
