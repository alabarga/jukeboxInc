import requests
import json
from datetime import datetime


class TinyBird():
      
    def __init__(self):
        with open('./credentials/tinybird.json') as f:
            credentials = json.load(f)

        self.token = credentials['token']

    def send_event(self, table, data):
                
        r = requests.post('https://api.tinybird.co/v0/events', 
        params = {
          'name': f'{table}',
          'token': f'{self.token}',
        }, 
        data=json.dumps(data)
        )

        return r
    
    def send_events(self, table, events):
                
        r = requests.post('https://api.tinybird.co/v0/events', 
        params = {
          'name': f'{table}',
          'token': f'{self.token}',
        }, 
        data = '\n'.join([json.dumps(ev) for ev in events])
        )

        return r

   
    def test(self):
          
        data = {
            'date': datetime.now().isoformat(),
            'city': 'Pretoria',
        }

        resp = self.send_event('events_example', data)

        print(resp.status_code)
        print(resp.text)

    def device_purchased(self, id, at):
          
        data= {
            "DeviceId": id,
            "DeviceDetails": {
              "DevicePrice": 500,
              "DeviceTypeName": "MusicMaker3000",
              "DeviceTypeId": "1",
              "SerialNumber": id
            },
            "OccurredAt": f"{at.isoformat()}"
          }

        self.send_event('device_purchased', data)

    def song_listened(self, track_id, device_id, duration, at):
          
        data= {    
                  "SongId": track_id,    
                  "DeviceId": device_id,    
                  "SongCompletedTime": duration,    
                  "OccurredAt": f"{at.isoformat()}"   
              }

        self.send_event('song_listened', data)

    def songs_listened(self, device_id, tracks):
          
        data= [ {    
                  "SongId": t['id'],    
                  "DeviceId": device_id,    
                  "SongCompletedTime": t['duration'],    
                  "OccurredAt": t['at'].isoformat()  
              } for t in tracks]

        self.send_events('song_listened', data)

    def song_published(self, track, at):
          
        data= {    
                  "SongId": track['id'],
                  "SongDetails": {
                    "ArtistName": track['artist'],
                    "SongName": track['name'],
                    "AlbumName": track['album'],
                    "SongLength": track['duration'], #"4:15",
                    "SongSizeMb": track['duration'] #8.5
                  },
                  "OccurredAt": at.isoformat()
              }

        self.send_event('song_listened', data)

    def song_occurred(self, track_id, at):
          
        data= {    
                  "SongId": track_id,    
                  "OccurredAt": f"{at.isoformat()}"   
              }

        self.send_event('song_listened', data)  
                 
    def payment_received(self, payment_id, customer_id, amount, at):
          
        data= {    
                  "PaymentId": payment_id,
                  "CustomerId": customer_id,
                  "PaymentAmount": amount,
                  "OccurredAt": at.isoformat()  
              }

        self.send_event('payment_received', data)

    def customer_registered(self, customer_id, at):
          
        data= {    
                  "CustomerId": customer_id,
                  "LegalAddress": "1, Waiyaki Way, Nairobi, Kenya",
                  "CustomerName": "Benedict Otieno",
                  "CustomerPhoneNumber": "07956678902",
                  "CustomerEmail": "me@gmail.com",
                  "CustomerIdentityNumber": "123456789",
                  "CustomerDateOfBirth": "12/12/1990",
                  "OccurredAt": at.isoformat()
              }

        self.send_event('customer_registered', data)

    def location_registered(self, customer_id, location_id, at):
              
        data= {
            "LocationId": location_id,
            "CustomerId": customer_id,
            "Latitude": "13.1339",
            "Longitude": "27.8493",
            "ContactName": "John Smith",
            "ContactPhoneNumber": "+254123456789",
            "OccurredAt": at.isoformat()
        }

        self.send_event('location_registered', data)

    def device_allocated(self, agent, device_id, location_id, at):
          
        data= {
                "DeviceId": device_id,
                "LocationAllocatedId": location_id,
                "SellingAgent":
                    {
                        "AgentId": agent['id'],
                        "AgentName": agent['name']
                    },
                "DeviceDetails": {
                    "DevicePrice": 700,
                    "DeviceName": "MusicMaker3000",
                    "Id": device_id
                },
                "OccurredAt": f"{at.isoformat()}"  
            }

        self.send_event('device_allocated', data)

