## Step 1
import json
import pandas as pd 
import os
import datetime
import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface

print("Read Shape file")
shp = shapefile.Reader(os.path.join(os.getcwd(), "shapefile", "ne_50m_admin_0_countries.shp")) #open the shapefile
all_shapes = [shape(_shape) for _shape in shp.shapes()] # get all the polygons
all_records = shp.records()
print("Done")

def getCountry(row):
    point = (row[1],row[0])
    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # get a boundary polygon
        if Point(point).within(boundary): # make a point and see if it's in the polygon
            name = all_records[i][-18] # get contry name from corresponding record , -18 = country name in english
            return name
# ------------------- Files iteration -----------------------
columns = ["latitude_deg","longitude_deg"] # lat and long column name
data_files = os.listdir(os.path.join(os.getcwd(), "data"))
result_path = os.path.join(os.getcwd(), "result")
if not os.path.exists(result_path):
    os.makedirs(result_path)
    
for data_csv in data_files:

    if not ".csv" in data_csv: continue

    print('-----------------')
    print(data_csv)
    print('-----------------')

    # Add column name
    print("Read data file")
    data = pd.read_csv(os.path.join(os.getcwd(), "data", data_csv), sep=",")
    loc_data = data[columns]
    print("Done")

    print("Tag country")
    loc_data["country"] = loc_data[["latitude_deg","longitude_deg"]].apply(getCountry, axis=1)
    country_count = loc_data.groupby('country').size().astype(int)
    country_count = dict(country_count)
    # Convert int64 to int to make dict JSON serializable
    for key in country_count:
        country_count[key] = int(country_count[key])

    with open(os.path.join(os.getcwd(), "country-count.json"), 'w') as fp:
        json.dump(country_count, fp)

    loc_data.to_csv(os.path.join(result_path, datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".csv"), index=False)
    print("Done")