import tkinter as tk
from tkinter.ttk import *
import boto3
import json
import simplejson
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

client = boto3.resource(
    'dynamodb',
    aws_access_key_id='AWS access key',
    aws_secret_access_key='AWS secret key',
    region_name='us-east-1'
)

temp = client.Table('DataSensing')

def sensing():

    data = temp.scan(AttributesToGet=['id', 'ftemp'],
                     Select='SPECIFIC_ATTRIBUTES'
                     )
    lines = sorted(data['Items'], key=lambda k: k['id'], reverse=False)

    count = 0
    for i in lines:
        convertJSON = json.dumps(i, cls=DecimalEncoder)
        temperature = simplejson.loads(convertJSON)['ftemp']
        tempId = simplejson.loads(convertJSON)['id']
        count+=1

    TempLabel['text'] = float(temperature)
    win.after(1000, sensing)

win = tk.Tk()
win.geometry("600x300+30+30")
win.configure(background='gray')
win.title("FGCU BioGas Temperature Sensing")

Title = Label(win,
              font="arial 24 bold",
              background='gray',
              text="FGCU BioGas Temperature Sensing")
Title.pack()

TempLabel = Label(win,
                  relief="ridge",
                  font="fixedsys 64 bold",
                  text='0.00')
TempLabel.place(x=215, y=210, anchor='sw')

sensing()
win.mainloop()
