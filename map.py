import sys
import subprocess
import pkg_resources

required = {'folium'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'folium'])

required = {'pandas'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'folium'])

import folium
import pandas

#----------------------------------
############  Map obj  ############
#----------------------------------

mymap=folium.Map(location=[41.531421, -99.203436],
zoom_start=5,
tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)

#----------------------------------
###########  Volcanoes  ###########
#----------------------------------

featureGroupVolc=folium.FeatureGroup(name='Volcanoes')

dataframe = pandas.read_csv("files/volcanoes.txt")
lat=[i for i in dataframe['LAT']]
lon=[i for i in dataframe['LON']]
names=[i for i in dataframe['NAME']]
loc=[i for i in dataframe['LOCATION']]
types=[i for i in dataframe['TYPE']]
el=[i for i in dataframe['ELEV']]



def getcolor(elevation): #Getcolor Function
        if elevation >= 3000:
            color='red'
        elif 1000 < elevation < 3000:
            color='green'
        else:
            color='#7c9eff'
        return color

for latt, long, name, location, type, elevation  in zip(lat, lon, names, loc, types, el):

    featureGroupVolc.add_child(folium.CircleMarker(location=[latt, long],
    radius=7,
    weight=1,
    opacity=0.6,
    fill_color=getcolor(elevation),
    fill_opacity=0.8,
    popup=folium.Popup(html=f'This is the {name} {type.lower()}. It is located in {location}. Its elevation is {int(elevation)} m.', max_width=300),
    color="black",
    shadow=True))

#----------------------------------


#----------------------------------
###########  Population  ##########
#----------------------------------

featureGroupPop=folium.FeatureGroup(name='Population')

featureGroupPop.add_child(folium.GeoJson(data=open("files/world.json", "r", encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor' : 'green' if x['properties'] ['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'},
popup=folium.GeoJsonPopup(fields=["POP2005"], labels=False, max_width=300)))

#----------------------------------


#----------------------------------
######  Adding FeatureGroups  #####
#----------------------------------

mymap.add_child(featureGroupPop)
mymap.add_child(featureGroupVolc)
mymap.add_child(folium.LayerControl())

#----------------------------------


mymap.save('World_population_and_volcanoes.html')
