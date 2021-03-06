from pymongo import MongoClient
from blessings import Terminal
import time, sys
from datetime import datetime

t = Terminal()

class Hue:
    __json_data = None
    __config = None

    def __init__(self, json_data, config):
        self.__json_data = json_data
        self.__config = config

    def sensors(self):
        client = MongoClient(self.__config['mongodb']['ip'], int(self.__config['mongodb']['port']))
        db = client.smarthome

        for key, value in self.__json_data.items():
            now_date = datetime.now()

            sensors = {}
            for sensor in value['sensors']:
                sensors[str(sensor['state']['type'].lower())] = {
                    'value' : sensor['state']['value'],
                    'id' : sensor['id']
                }

            cursor = db.sensors.find_one({"uniqueid":key})
            if(cursor is not None):
                resualt = db.sensors.update_one({
                    'uniqueid' : str(key),
                },{
                    '$set' : {
                        'battery' : int(value['battery']),
                        'sensors' : sensors,
                        'updated_at' : now_date
                    }
                })

                print t.blue('[UPDATE] uniqueid: '+ str(key) +' | time: '+ now_date.strftime("%Y-%m-%d %H:%M:%S"))

            else:
                resualt = db.sensors.insert_one({
                    'uniqueid' : str(key),
                    'battery' : int(value['battery']),
                    'sensors' : sensors,
                    'updated_at' : now_date,
                    'created_at' : now_date
                })

                print t.blue('[INSERT] uniqueid: '+ str(key) +' | time: '+ now_date.strftime("%Y-%m-%d %H:%M:%S"))

        client.close()

    def lights(self):
        client = MongoClient(self.__config['mongodb']['ip'], int(self.__config['mongodb']['port']))
        db = client.smarthome

        for value in self.__json_data:
            now_date = datetime.now()

            cursor = db.lights.find_one({"uniqueid": str(value['uniqueid'])})

            print value

            hue_bri = int(value['state']['bri'])
            hue_on = True if bool(value['state']['on']) == True and hue_bri > 0 else False



            if(cursor is not None):
                resualt = db.lights.update_one({
                    'uniqueid' : str(value['uniqueid']),
                },{
                    '$set' : {
                        'id' : value['id'],
                        'swversion' : value['swversion'],
                        'name' : value['name'].encode('utf-8'),
                        'state' : {
                            'on' : value['state']['on'],
                            'bri' : value['state']['bri'],
                            'hue' : value['state']['hue'],
                            'ct' : value['state']['ct'],
                            'sat' : value['state']['sat'],
                            'colormode' : value['state']['colormode'],
                            'effect' : value['state']['effect'],
                            'alert' : value['state']['alert'],
                            'reachable' : value['state']['reachable'],
                            'xy' : {
                                'x' : value['state']['xy']['x'],
                                'y' : value['state']['xy']['y']
                            }
                        },
                        'updated_at' : now_date
                    }
                })

                print t.blue('[UPDATE] uniqueid: '+ str(value['uniqueid']) +' | time: '+ now_date.strftime("%Y-%m-%d %H:%M:%S"))

            else:
                resualt = db.lights.insert_one({
                    'id' : value['id'],
                    'swversion' : value['swversion'],
                    'uniqueid' : value['uniqueid'],
                    'modelid' : value['modelid'],
                    'manufacturer' : value['manufacturer'],
                    'name' : value['name'].encode('utf-8'),
                    'type' : value['type'],
                    'state' : {
                        'on' : value['state']['on'],
                        'bri' : value['state']['bri'],
                        'hue' : value['state']['hue'],
                        'ct' : value['state']['ct'],
                        'sat' : value['state']['sat'],
                        'colormode' : value['state']['colormode'],
                        'effect' : value['state']['effect'],
                        'alert' : value['state']['alert'],
                        'reachable' : value['state']['reachable'],
                        'xy' : {
                            'x' : value['state']['xy']['x'],
                            'y' : value['state']['xy']['y']
                        }
                    },
                    'updated_at' : now_date,
                    'created_at' : now_date
                })

                print t.blue('[INSERT] uniqueid: '+ str(value['uniqueid']) +' | time: '+ now_date.strftime("%Y-%m-%d %H:%M:%S"))
