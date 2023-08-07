# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import pandas as pd
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy import read_events
import numpy as np

def read_csv(csv_file,  datenum= True, **kwargs):
    
    # df = pd.read_csv(csv_file, engine="pyarrow", **kwargs) #use pyarrow for faster input
    df = pd.read_csv(csv_file, **kwargs)
    
    df.columns= df.columns.str.lower() # convert header to all lowercase letters
    header = df.columns
    
    # replace with common column names if present
    if 'time' in header:
        t_label = 'time'
    elif 't' in header:
        t_label = 't'

    if 'lon' in header:
        x_label = 'lon'
    elif 'long' in header:
        x_label = 'long'
    elif 'longitude' in header:
        x_label = 'longitude'
    elif 'x' in header:
        x_label = 'x'
        
    if 'lat' in header:
        y_label = 'lat'
    elif 'latitude' in header:
        y_label = 'latitude'
    elif 'y' in header:
        y_label = 'y'

    if 'depth' in header:
        z_label = 'depth'
    elif 'z' in header:
        z_label = 'z'

    if 'mag' in header:
        mag_label = 'mag'    
    elif 'ml' in header:
        mag_label = 'ml'
    elif 'magnitude' in header:
        mag_label = 'magnitude'

    t_raw = df[t_label].to_numpy()
    lat = df[y_label].to_numpy()
    lon = df[x_label].to_numpy()
    depth = df[z_label].to_numpy()
    mag = df[mag_label].to_numpy()
    
    if datenum:    
        timestamps = pd.to_datetime(t_raw-719529, unit='D') #convert from Matlab's datenum format to human readable format
        
    time = timestamps.to_numpy() # get time as numpy datetime64 objects
    time = [UTCDateTime(str(t)) for t in time] # convert to list of obspy UTCDateTime objects
    
    return time, lat, lon, depth, mag


def read_fdsn(service, save_to_file=None, file_format="QUAKEML", **kwargs):
       
    client = Client(service)    
    cat = client.get_events(**kwargs)
    
    if save_to_file != None:
        cat.write(filename=save_to_file, format=file_format, **kwargs)
    
    return extract_from_obspy_cat(cat)


def read_obspy(file, **kwargs):
    
    cat = read_events(file)
    
    return extract_from_obspy_cat(cat)


def extract_from_obspy_cat(cat):
    
    mag = np.array([event.preferred_magnitude().mag for event in cat])
    time = [event.preferred_origin().time for event in cat]
    lat = [event.preferred_origin().latitude for event in cat]
    lon = [event.preferred_origin().longitude for event in cat]
    depth = [event.preferred_origin().depth for event in cat]
    
    return time, lat, lon, depth, mag