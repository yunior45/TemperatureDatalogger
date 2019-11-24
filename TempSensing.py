import glob
import time
import boto3
from boto3.dynamodb.conditions import Key
from decimal import *
from string import *

randomId = 0

client = boto3.resource(
    'dynamodb',
    aws_access_key_id='AWS access key',
    aws_secret_access_key= 'AWS secret key',
    region_name='us-east-1'
)

tempTable = client.Table('DataSensing')

data = temp.scan(AttributesToGet=['id', 'ftemp'])
lines = sorted(data['Items'], key=lambda k: k['id'], reverse=False)

for i in lines:
    randomId += 1

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def rawTemp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def tempRead():
    lines = rawTemp()
    while lines[0].strip()[-3:] != 'YES':
       time.sleep(0.2)
       lines = rawTemp()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp = (float(temp_string)/1000.0) * 9.0 / 5.0 + 32.0
        return temp


while True:
    ftemp = tempRead()

    tempTable.put_item(
        Item={
              "ftemp": str(round(ftemp, 1)),
	          "id": randomId
        }
    )
    randomId += 1
    time.sleep(5)
