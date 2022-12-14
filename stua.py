import aiohttp, asyncio
#import ray
import requests, csv, datetime, math, os, json, calendar
import time as te
from abc import ABC, abstractmethod
from xml.etree.ElementTree import fromstring, ElementTree as ET
import gtfs_realtime_pb2, nyct_subway_pb2


APIMTA = ""
APIBUSTIME = ""

class gtfs(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set(self):
        pass

    @abstractmethod
    def get(self):
        pass

class gtfsSubway(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.trip_id = ""

    def set(self, route_id, terminus, terminus_id, station, station_id, direction, time, pattern, description, trip_id):
        self.route_id = route_id
        self.terminus = terminus#_id)
        self.terminus_id = terminus_id
        self.station = station#_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.trip_id = trip_id

    def get(self, station, direction, responses, batched=False):
        _validkeySubway(_getAPIMTA())
        _responseIndex(responses)
        output = _transitSubway(station, direction, responses, _getAPIMTA())
        #print(output)
        if (output == "NO TRAINS"):
            self.route_id = "X"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertSubway(station)
            self.station_id = station
            self.direction = direction
            self.time = -1
            descriptions = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.service_description = "NO TRAINS"
            self.trip_id = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertSubway(output[2][:-1])
            self.terminus_id = output[2]
            self.station = convertSubway(output[3])
            self.station_id = output[3]
            self.direction = output[4]
            self.time = output[0]
            descriptions = _routes(output[1])
            self.service_pattern = descriptions[0]
            self.service_description = descriptions[1]
            self.trip_id = output[5]

class gtfsBus(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = ""
        self.stop_id = ""
        self.time = ""
        self.service_pattern = ""
        self.direction = 0
        self.trip_id = ""
        self.vehicle = ""

    def get(self, stop, direction, responses):
        _validkeyBus(_getAPIBUSTIME())
        _responseIndex(responses)
        output = _transitBus(stop, direction, responses, _getAPIBUSTIME())
        if (output == "NO BUSES"):
            self.route_id = "NO BUSES"
            self.terminus = "NO BUSES"
            self.terminus_id = "NO BUSES"
            self.stop = stop
            self.stop_id = convertBus(stop)
            self.time = -1
            self.service_pattern = "NO BUSES"
            self.direction = direction
            self.trip_id = "NO BUSES"
            self.vehicle = "NO BUSES"
        else:
            self.route_id = output[1]
            self.terminus = output[5]
            self.terminus_id = output[2]
            self.stop = output[4]
            self.stop_id = output[3]
            self.time = output[0]
            self.service_pattern = output[7]
            self.direction = output[6]
            self.trip_id = output[8]
            self.vehicle = output[9]

    def set(self, route_id, terminus, terminus_id, stop, stop_id, time, service_pattern, direction, trip_id, vehicle):
        self.route_id = route_id
        self.terminus = terminus
        self.terminus_id = terminus_id
        self.stop = stop
        self.stop_id = stop_id
        self.time = time
        self.service_pattern = service_pattern
        self.direction = direction
        self.trip_id = trip_id
        self.vehicle = vehicle

class gtfsLIRR(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.station_id_list = ""
        self.station_name_list = ""
        self.trip_id = ""
        self.vehicle = ""

    def get(self, stop, direction, responses):
        _validkeySubway(_getAPIMTA())
        _responseIndex(responses)
        output = _transitLIRR(stop, direction, responses, _getAPIMTA())
        if (output == "NO TRAINS"):
            self.route_id = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertLIRR(stop)
            self.station_id = stop
            self.time = -1
            self.service_description = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.station_id_list = "NO TRAINS"
            self.station_name_list = "NO TRAINS"
            self.direction = direction
            self.trip_id = "NO TRAINS"
            self.vehicle = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertLIRR(output[2])
            self.terminus_id = output[2]
            self.station = convertLIRR(output[3])
            self.station_id = output[3]
            self.time = output[0]
            self.service_description = f"{_timeconvert(output[0])} train to " + convertLIRR(output[2])
            self.service_pattern = convertLIRR(output[2])
            self.station_id_list = output[6]
            self.station_name_list = output[7]
            self.direction = output[4]
            self.trip_id = output[5]
            self.vehicle = output[8]

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id, station_id_list, vehicle):
        self.route_id = route_id
        self.terminus = convertLIRR(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertLIRR(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.station_id_list = station_id_list
        self.station_name_list = [convertLIRR(i) for i in station_id_list]
        self.trip_id = trip_id
        self.vehicle = vehicle

class gtfsMNR(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.station_id_list = ""
        self.station_name_list = ""
        self.trip_id = ""
        self.vehicle = ""

    def get(self, stop, direction, responses):
        _validkeySubway(_getAPIMTA())
        _responseIndex(responses)
        output = _transitMNR(stop, direction, responses, _getAPIMTA())
        if (output == "NO TRAINS"):
            self.route_id = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertMNR(stop)
            self.station_id = stop
            self.time = -1
            self.service_description = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.station_id_list = "NO TRAINS"
            self.station_name_list = "NO TRAINS"
            self.direction = direction
            self.trip_id = "NO TRAINS"
            self.vehicle = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertMNR(output[2])
            self.terminus_id = output[2]
            self.station = convertMNR(output[3])
            self.station_id = output[3]
            self.time = output[0]
            self.service_description = f"{_timeconvert(output[0])} train to " + convertMNR(output[2])
            self.service_pattern = convertMNR(output[2])
            self.station_id_list = output[6]
            self.station_name_list = output[7]
            self.direction = output[4]
            self.trip_id = output[5]
            self.vehicle = output[8]

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id, station_id_list, vehicle):
        self.route_id = route_id
        self.terminus = convertMNR(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertMNR(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.station_id_list = station_id_list
        self.station_name_list = [convertMNR(i) for i in station_id_list]
        self.trip_id = trip_id
        self.vehicle = vehicle

class gtfsFerry(gtfs):
    def __init__(self):
        self.route_id_SN = ""
        self.route_id_LN = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = "" 
        self.stop_id = ""
        self.time = 0
        self.trip_id = ""
        self.vehicle = ""

    def get(self, stop, responses):
        _responseIndex(responses)
        output = _transitFerry(stop, responses)
        if (output == "NO FERRIES"):
            self.route_id_SN = "NO FERRIES"
            self.route_id_LN = "NO FERRIES"
            self.terminus = "NO FERRIES"
            self.terminus_id = "NO FERRIES"
            self.stop = convertFerry(stop)
            self.stop_id = stop
            self.time = -1
            self.trip_id = "NO FERRIES"
            self.vehicle = "NO FERRIES"
        else:
            self.route_id_SN = output[7]
            self.route_id_LN = output[8]
            self.terminus = convertFerry(output[1])
            self.terminus_id = output[1]
            self.stop = convertFerry(output[2])
            self.stop_id = output[2]
            self.time = output[0]
            self.trip_id = output[3]
            self.vehicle = output[6]

    def set(self, route_id_SN, route_id_LN, terminus_id, stop_id, time, trip_id, vehicle):
        self.route_id_SN = route_id_SN
        self.route_id_LN = route_id_LN
        self.terminus = convertFerry(terminus_id)
        self.terminus_id = terminus_id
        self.stop = convertFerry(stop_id)
        self.stop_id = stop_id
        self.time = time
        self.trip_id = trip_id
        self.vehicle = vehicle

class gtfsPATH(gtfs):
    def __init__(self):
        self.route = ""
        self.terminus = ""
        self.station = "" 
        self.direction = ""
        self.time = 0
        self.status = ""

    def set(self, route, terminus, station, direction, time, status):
        self.route = ""
        self.terminus = ""
        self.station = "" 
        self.direction = ""
        self.time = 0
        self.status = ""

    def get(self, station, responses):
        _responseIndex(responses)
        output = _transitPATH(station.lower(), responses)
        #print(output)
        if (output == "NO TRAINS"):
            self.route = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.station = "NO TRAINS" 
            self.direction = "NO TRAINS"
            self.time = -1
            self.status = "NO TRAINS"
        else:
            self.route = output[1]
            self.terminus = output[2]
            self.station = output[3]
            self.direction = output[4]
            self.time = output[0]
            self.status = output[5]

def _responseIndex(index):
    if (index <= 0):
        raise Exception("INVALID RESPONSES INDEX, MUST BE > 0")

def sort(objects):
    if (objects == []):
        return False
    for i in objects:
        if (hasattr(i, "time") == False):
            return False
    objects.sort(key = lambda x: x.time)
    return True

def keyMTA(string):
    global APIMTA
    APIMTA = string 

def keyBUSTIME(string):
    global APIBUSTIME
    APIBUSTIME = string 

def _getAPIMTA():
    return APIMTA

def _getAPIBUSTIME():
    return APIBUSTIME

def _timeconvert(input):
    out = datetime.datetime.now() + datetime.timedelta(minutes=input) 
    return out.strftime('%H:%M')

def _validkeySubway(key):
    if (str(requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs", headers={'x-api-key' : key}))) != "<Response [200]>":
        raise Exception("INVALID KEY")

def _validkeyBus(key):
    if (str(requests.get(f'http://bustime.mta.info/api/where/stop/MTA_550320.xml?key={key}'))) != "<Response [200]>":
        raise Exception("INVALID KEY")

def convertBus(input):
    if type(input) != type("") and type(input) != type(0):
        raise Exception("INVALID CLASS: This method requires a String or an Integer")
    if (type(input) == type(0)):
        input = str(input)
    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{input}.xml?key={_getAPIBUSTIME()}')
    tree = ET(fromstring(responsestop.content))
    root = tree.getroot()
    stop_name = root[4][4].text
    return stop_name

def convertSubway(input):
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    output = []
    with open('stops.txt','r') as csv_file:
        if (len(input) == 3):
            csv_file = csv.reader(csv_file)
            for row in csv_file:
                if row[2] == input:
                    output.append(row[5])
        else:
   
            raise Exception("INVALID ARGUMENT")
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

def convertLIRR(input):
    output = ""
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    if (type(input) == type(0)):
        input = str(input)
    #print(input)
    f = open("lirr_gtfs.json")
    data = json.load(f)
    #print(data["gtfs"]["stops"])
    for i in data["gtfs"]["stops"]:
        if input == i["stop_id"]:
            output = i["stop_name"]
    #print(output)
    return output 

def convertMNR(input):
    output = ""
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    if (type(input) == type(0)):
        input = str(input)
    #print(input)
    with open('stations.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == input:
               output = row[2]
    #print(output)
    return output

def convertFerry(input):
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    output = []
    with open('ferry_stops.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == input:
                output.append(row[2])
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

async def _requestMTA(session, url, API):
    async with session.get(url, headers={'x-api-key' : API}) as response:
        data = await response.read()
    return data

async def _requestFeedMTA(sites, API):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(_requestMTA(session, url, API))
            tasks.append(task)
        out = await asyncio.gather(*tasks, return_exceptions=True)
        return out

async def _requestBustime(session, url):
    async with session.get(url) as response:
        #print(response)
        data = await response.read()
    return data

async def _requestFeedBustime(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(_requestBustime(session, url))
            tasks.append(task)
        out = await asyncio.gather(*tasks, return_exceptions=True)
        return out

def _url():
    link = []
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs')
    return link

def _transitSubway(stop, direction, responses, API, id="NONE"):
    times = []
    destination = []
    current_time = datetime.datetime.now()
    links = asyncio.get_event_loop().run_until_complete(_requestFeedMTA(_url(), API))

    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(link)
        #print(str(feed))
        
        '''
        with open(f"logs/NYCT_GTFS/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
            test.write(str(feed)+ f" {datetime.datetime.now()}\n")
        '''
        #print(str(feed))
        
        for entity in feed.entity:
            #print(entity)
            for update in entity.trip_update.stop_time_update:
                if (update.stop_id == stop+direction):
                    station_id = update.stop_id[:-1]
                    direction = update.stop_id[-1]
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                    #print(time)
                    if (time < 0):
                        continue 
                    trip_id = entity.trip_update.trip.trip_id
                    route_id = entity.trip_update.trip.route_id
                    if (id != "NONE" and id != route_id):
                        continue
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                    #print(service_description)
                    terminus_id = destination[-1]
                    #print(terminus_id)
                
                    #print(stop)
                    times.append([time, route_id, terminus_id, station_id, direction, trip_id])

    #print(times)
    times.sort()
    #times = []
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times

def _transitSubwayMODDED(stops, API):
    final = []
    current_time = datetime.datetime.now()
    links = asyncio.get_event_loop().run_until_complete(_requestFeedMTA(_url(), API))
    for stop in stops:
        times = []
        destination = []
        for link in links:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(link)
            
            '''
            with open(f"logs/NYCT_GTFS/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
                test.write(str(feed)+ f" {datetime.datetime.now()}\n")
            '''
            #print(str(feed))
            
            for entity in feed.entity:
                #print(entity)
                for update in entity.trip_update.stop_time_update:
                    if (update.stop_id == stop[0]+stop[1]):
                        station_id = update.stop_id[:-1]
                        direction = update.stop_id[-1]
                        time = update.arrival.time
                        if (time < 0):
                            time = update.departure.time
                        time = datetime.datetime.fromtimestamp(time)
                        time = math.trunc(((time - current_time).total_seconds()) / 60)
                        #print(time)
                        if (time < stop[3]):
                            continue 
                        trip_id = entity.trip_update.trip.trip_id
                        route_id = entity.trip_update.trip.route_id
                        if (stop[4] != "NONE" and stop[4] != route_id):
                            continue
                        for update in entity.trip_update.stop_time_update:
                            destination.append(update.stop_id)
                        #print(service_description)
                        terminus_id = destination[-1][:-1]
                        
                        #print(stop)
                        #times.append([time, route_id, terminus_id, station_id, direction, trip_id])
                        train = gtfsSubway()
                        description = _routes(route_id)
                        train.set(route_id, convertSubway(terminus_id), terminus_id, convertSubway(station_id), station_id, direction, time, description[0], description[1], trip_id)
                        times.append(train)

    #print(times)
        sort(times)
        #times = []
        try:
            final.append(times[stop[2]-1])
        except:
            #final.append("NO TRAINS")
            train = gtfsSubway()
            train.set("NO TRAINS", "NO TRAINS", "NO TRAINS", "NO TRAINS", stop[0], stop[1], -1, "NO TRAINS", "NO TRAINS", "NO TRAINS")
            final.append(train)
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return final
    

def _transitBus(stop, direction, responses, API, id="NONE"):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    links = asyncio.get_event_loop().run_until_complete(_requestFeedBustime([f"http://gtfsrt.prod.obanyc.com/tripUpdates?key={API}"]))
    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(link)
        #print(feed)
 
        for entity in feed.entity:
            for update in entity.trip_update.stop_time_update:
        
                if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
            
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                    if (time < 0):
                        continue 
                    trip_id = entity.trip_update.trip.trip_id
                    route_id = entity.trip_update.trip.route_id
                    if (id != "NONE" and id != route_id):
                        continue
                    vehicle = entity.trip_update.vehicle.id[-4:]
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                    terminus_id = destination[-1]
                    direction = entity.trip_update.trip.direction_id
                    stop_id = update.stop_id
            
                    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{stop}.xml?key={API}')
                    #filenamevar = f"bustime.xml"
            
                    #with open(filenamevar,"wb") as f:
                    #    f.write(responsestop.content)
                    tree = ET(fromstring(responsestop.content))
                    # tree = ET.parse(filenamevar)
                    root = tree.getroot()
                    stop_name = root[4][4].text
                    for item in root[4][7]:
                        if (item[1].text == route_id):
                            service_pattern = item[3].text
                    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{terminus_id}.xml?key={API}')
                    #filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
                    #filenamevar = f"bustime.xml"
                    tree = ET(fromstring(responsestop.content))
                    # tree = ET.parse(filenamevar)
                    #root = tree.getroot()
                    root = tree.getroot()
                    terminus_name = root[4][4].text
                
                    times.append([time, route_id, terminus_id, stop_id, stop_name, terminus_name, direction, service_pattern, trip_id, vehicle])
                    
    times.sort()
    try:
        times = times[responses-1]
    except:
        return "NO BUSES"
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times

def _transitBusMODDED(stops, API):
    final = []
    current_time = datetime.datetime.now()
    link = requests.get(f"http://gtfsrt.prod.obanyc.com/tripUpdates?key={API}")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(link.content)
    for stop in stops:
        times = []
        destination = []
       
        for entity in feed.entity:
            for update in entity.trip_update.stop_time_update:
        
                if ((update.stop_id == stop[0]) and (str(entity.trip_update.trip.direction_id) == str(stop[1]))):
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                    if (time < stop[3]):
                        continue 
                    trip_id = entity.trip_update.trip.trip_id
                    route_id = entity.trip_update.trip.route_id
                    if (stop[4] != "NONE" and stop[4] != route_id):
                        continue
                    vehicle = entity.trip_update.vehicle.id[-4:]
                    stop_id = update.stop_id
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                    terminus_id = destination[-1]
                    #print(terminus_id)
                    direction = entity.trip_update.trip.direction_id
            
                    
                    
                    """
                    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{stop}.xml?key={API}')
                    #filenamevar = f"bustime.xml"
            
                    #with open(filenamevar,"wb") as f:
                    #    f.write(responsestop.content)
                    tree = ET(fromstring(responsestop.content))
                    # tree = ET.parse(filenamevar)
                    root = tree.getroot()
                    stop_name = root[4][4].text
                    for item in root[4][7]:
                        if (item[1].text == route_id):
                            service_pattern = item[3].text
                    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{terminus_id}.xml?key={API}')
                    #filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
                    #filenamevar = f"bustime.xml"
                    tree = ET(fromstring(responsestop.content))
                    # tree = ET.parse(filenamevar)
                    root = tree.getroot()
                    root = tree.getroot()
                    terminus_name = root[4][4].text
                    """

                    bus = gtfsBus()
                    bus.set(route_id, f'http://bustime.mta.info/api/where/stop/MTA_{terminus_id}.xml?key={API}', terminus_id, f'http://bustime.mta.info/api/where/stop/MTA_{stop_id}.xml?key={API}', stop_id, time, "", direction, trip_id, vehicle)
                    times.append(bus)
                    
        sort(times)
        try:
            final.append(times[stop[2]-1])
        except:
            bus = gtfsBus()
            bus.set("NO BUSES", "NO BUSES", "NO BUSES", "NO BUSES", "NO BUSES", -1, "NO BUSES", "NO BUSES", "NO BUSES", "NO BUSES")
            final.append(bus)

    download = []
    for item in final:
        download.append(item.stop)
        #print(item.stop_id)
        download.append(item.terminus)
        #print(item.terminus_id)
    #print(download)
    download = asyncio.get_event_loop().run_until_complete(_requestFeedBustime(download))
    #print(len(download))
    for num in range(0, len(final)):
        try:
            #print(num)
            tree = ET(fromstring(download[num*2]))
            root = tree.getroot()
            stop_name = root[4][4].text
            for item in root[4][7]:
                if (item[1].text == route_id):
                    service_pattern = item[3].text
            final[num].stop = stop_name
            final[num].service_pattern = service_pattern
            
            tree = ET(fromstring(download[(num*2)+1]))
            root = tree.getroot()
            terminus_name = root[4][4].text
            final[num].terminus = terminus_name
        except:
            final[num].stop = "NO BUSES"
            final[num].service_pattern = "NO BUSES"
            final[num].terminus = "NO BUSES"

    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return final

def  _transitLIRR(stop, direction, responses, API):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    links = asyncio.get_event_loop().run_until_complete(_requestFeedMTA([f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr"], API))
    
    for link in links:
        #print(link)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(link)
        print(feed)
        for entity in feed.entity:
            for update in entity.trip_update.stop_time_update:
                if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
                    station_id = update.stop_id
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                    #print(time)
                    if (time < 0):
                        continue 
                    if entity.trip_update.trip.trip_id[-2] == "_":
                        vehicle = entity.trip_update.trip.trip_id
                        vehicle = vehicle.replace("_","")
                        vehicle = entity.trip_update.trip.trip_id[-6:-2]
                    else:
                        vehicle = entity.trip_update.trip.trip_id[-4:]
                    trip_id = entity.trip_update.trip.trip_id
                    route_id = entity.trip_update.trip.route_id
                    direction = entity.trip_update.trip.direction_id
                    station_id_list = []
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                        station_id_list.append(update.stop_id)
                    #print(service_description)
                    station_stop_list = [convertLIRR(i) for i in station_id_list]
                    terminus_id = destination[-1]
                
                    #print(stop)

                    times.append([time, route_id, terminus_id, station_id, direction, trip_id, station_id_list, station_stop_list, vehicle])
                    #print(times)
                    #print(data["gtfs"]["stops"])
                    #for i in data["gtfs"]["stops"]:
                    #print(i["stop_id"] + " " + i["stop_name"])
    times.sort()
    #times = []
    #print(times)
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times 

def  _transitMNR(stop, direction, responses, API):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    links = asyncio.get_event_loop().run_until_complete(_requestFeedMTA(_url(["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"]), API))
    
    for link in links:
    
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(link)

        for entity in feed.entity:
            for update in entity.trip_update.stop_time_update:
                if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
                    station_id = update.stop_id
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                    #print(time)
                    if (time < 0):
                        continue 
                    if entity.trip_update.trip.trip_id[-2] == "_":
                        vehicle = entity.trip_update.trip.trip_id
                        vehicle = vehicle.replace("_","")
                        vehicle = entity.trip_update.trip.trip_id[-6:-2]
                    else:
                        vehicle = entity.trip_update.trip.trip_id[-4:]
                    trip_id = entity.trip_update.trip.trip_id
                    route_id = entity.trip_update.trip.route_id
                    direction = entity.trip_update.trip.direction_id
                    station_id_list = []
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                        station_id_list.append(update.stop_id)
                    #print(service_description)
                    station_stop_list = [convertMNR(i) for i in station_id_list]
                    terminus_id = destination[-1]
                
                    #print(stop)

                    times.append([time, route_id, terminus_id, station_id, direction, trip_id, station_id_list, station_stop_list, vehicle])
                    #print(data["gtfs"]["stops"])
                    #for i in data["gtfs"]["stops"]:
                    #print(i["stop_id"] + " " + i["stop_name"])
    times.sort()
    #times = []
    #print(times)
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times 

def _transitFerry(stop, responses):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    response = requests.get("http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/tripupdate")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    '''
    with open(f"logs/NYCFerry/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
    '''
    for entity in feed.entity:
        for update in entity.trip_update.stop_time_update:
            #print(update.stop_id)
            if (update.stop_id == stop):
                #print("checkpointA")
                station_id = update.stop_id
                time = update.arrival.time
                if (time < 0):
                    time = update.departure.time
                time = datetime.datetime.fromtimestamp(time)
                time = math.trunc(((time - current_time).total_seconds()) / 60)
                #print(time)
                if (time < 0):
                    continue 
                trip_id = entity.trip_update.trip.trip_id
                station_id_list = []
                for update in entity.trip_update.stop_time_update:
                    destination.append(update.stop_id)
                    station_id_list.append(update.stop_id)
                #print(service_description)
                station_stop_list = [convertFerry(i) for i in station_id_list]
                terminus_id = destination[-1]
                vehicle = entity.trip_update.vehicle.label

                with open('ferry_trips.txt','r') as csv_file:
                    csv_file = csv.reader(csv_file)
                    for row in csv_file:
                        if row[2] == trip_id:
                            route_id_SN = row[0]

                with open('ferry_routes.txt','r') as csv_file:
                    csv_file = csv.reader(csv_file)
                    for row in csv_file:
                        if row[0] == route_id_SN:
                            route_id_LN = row[3]
            
                #print(stop)

                times.append([time, terminus_id, station_id, trip_id, station_id_list, station_stop_list, vehicle, route_id_SN, route_id_LN])
                #print(data["gtfs"]["stops"])
                #for i in data["gtfs"]["stops"]:
                #print(i["stop_id"] + " " + i["stop_name"])
    times.sort()
    try:
        times = times[responses-1]
    except:
        return "NO FERRIES"
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times


#PATH STOP LIST
#newark
#harrison
#journal_square
#grove_street
#exchange_place
#world_trade_center
#newport
#hoboken
#christopher_street
#ninth_street
#fourteenth_street
#twenty_third_street
#thirty_third_street

def _transitPATH(stop, responses):
    current_time = datetime.datetime.now()
    times = []
    #print(API)
    response = requests.get(f"https://path.api.razza.dev/v1/stations/{stop}/realtime")
    feed = json.loads(response.content)
    '''
    with open(f"logs/NYCFerry/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
    '''
    for entity in feed["upcomingTrains"]:
        route = entity["route"]
        terminus = entity["headsign"]
        station = (stop.lower()).capitalize() 
        direction = entity["direction"]
        timestamp = te.strptime(entity["projectedArrival"], "%Y-%m-%dT%H:%M:%SZ")
        unix_time_utc = calendar.timegm(timestamp)
        time = datetime.datetime.fromtimestamp(unix_time_utc)
        time = math.trunc(((time - current_time).total_seconds()) / 60)
        status = entity["status"]
        times.append([time, route, terminus, station, direction, status])

    times.sort()
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)
    '''
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    '''
    return times
    

def _routes(service):
    with open('routes.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == service:
                return row[3], row[4], row[6]

def alertsSubway(planned=True):
    #print(planned)
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    """
    with open("logs/NYCT_GTFS/alerts.txt","w") as f:
        f.write(str(feed))
    """
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):     
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    #print(alerts)
    return alerts 

def alertsLIRR(planned=False):
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    with open("logs/LIRR/alerts.txt","w") as f:
        f.write(str(feed))
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):     
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    return alerts

def alertsMNR(planned=False):
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):     
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    return alerts

def alertsBus(planned=False):
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):     
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    return alerts

def alertsFerry():
    alerts = []
    response = requests.get("http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/alert")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):     
                if (entity.alert.header_text.translation):
                    for update in entity.alert.header_text.translation:
                        if update.language == "en-html":
                            alerts.append(entity.alert.header_text.translation[0].text)
    return alerts

def gtfsSubwayBATCHED(stops):
    output = _transitSubwayMODDED(stops, _getAPIMTA())
    return output

def gtfsBusBATCHED(stops):
    output = _transitBusMODDED(stops, _getAPIBUSTIME())
    return output