import numpy as np
from overturemaps import *
import overturemaps
import pandas
import geopandas as gpd
from shapely import wkb
from lonboard import *

bbox =-122.66, 37, -121.6, 38 #bbox for san fransisco
gdf = core.geodataframe("place", bbox=bbox)
categories = ["cafe","restaurant","car_dealer","florist"]
phones = []
biz = gdf[gdf.columns[7]]
biz_primary = biz.apply(lambda x: x.get('primary','N/A'))
biz_phones = gdf[gdf.columns[12]]
for category in categories:
  phone = []
  for i in range(len(biz)):
    if biz_primary[i] == category and gdf[gdf.columns[9]][i] == None:
      #print(gdf[gdf.columns[6]][i])
      phone.append(biz_phones[i]) 
  phone = [i for i in phone if i != None]
  phones.append(phone)
  print(f"Number of phone numbers found for {category} businesses without websites: ", len(phone))
for category in phones:
  for phone in category:
    if(len(phone[0]) == 12):
      print(phone[0])