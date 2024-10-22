import pandas as pd
import json
from datetime import datetime
import calendar
import time
import uuid
import sys
import pytz
from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.exceptions import EventHubError
from random import randint

tz_lima = pytz.timezone('America/Lima')


CONNECTION_STR = "Endpoint=sb://evhb-dam.servicebus.windows.net/;SharedAccessKeyName=admin;SharedAccessKey=K22uQmI8e/Jjv63AsCcs+Er8JGqxuyu3T+AEhAI9hTI=;EntityPath=evhb-dam"
EVENTHUB_NAME = "evhb-dam"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

def put_to_stream(producer):
        
    for _ in range(100000):
      event_data_batch = producer.create_batch()
      datetime_lima = datetime.now(tz_lima)
      temperature = 20 + randint(0,10)
      humidity = 10 + randint(0,10)
      record = {
          'id': str(uuid.uuid4()),
          'datetime': datetime_lima.strftime("%Y-%m-%d %H:%M:%S"),
          'temperature': temperature,
          'humidity' :  humidity
      }
      print(record)
      to_json= json.dumps(record)
      event_data_batch.add(EventData(to_json))
      producer.send_batch(event_data_batch)
      event_data_batch=""
      time.sleep(5) #Dormir cada 1 seg

put_to_stream(producer)
