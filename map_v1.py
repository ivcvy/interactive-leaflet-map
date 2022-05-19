# use geoplot to ease geospatial visualizations 
!pip install geoplot
import geoplot
print("Geoplot Version : {}".format(geoplot.__version__))

# use geopandas dataset to locate country coordinates
import geopandas as gpd
print("Geopandas Version : {}".format(gpd.__version__))
print("Available Datasets : {}".format(gpd.datasets.available))

# checking the naturalearth_lowres dataset
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.head()

# import dataframe
import pandas as pd
from io import StringIO

data = '''data goes here'''

df = pd.read_csv(StringIO(data))
df

# merging dataframe with geopandas dataset to get the locations
world_df = pd.merge(world, df, left_on="name", right_on="country", how="outer")

# remove antarctica
world_df = world_df[world_df.name != "Antarctica"]
world_df

# use folium to make leaflet map
import pandas as pd
import folium
import branca.colormap as cm

# determine the centroids or center coordinates for initial view
x_map=world_df['geometry'].centroid.x.mean()
y_map=world_df['geometry'].centroid.y.mean()
print(x_map,y_map)

# blank map with zoom level of 2 at start
mymap = folium.Map(location=[y_map, x_map], zoom_start=2,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
mymap

#creating choropleth map using multiple quantiles due to wide range of 'number' value
myscale = (world_df['number'].quantile((0,0.25,0.50,0.75,0.9,0.98,1))).tolist() #1,6,18,77,300,4456,7621
mymap.choropleth(
                  geo_data=world_df,
                  name='Choropleth',
                  data=world_df,
                  columns=['name','number'],
                  key_on="feature.properties.name",
                  fill_color='YlGnBu',
                  threshold_scale=myscale,
                  fill_opacity=1,
                  line_opacity=0.2, legends=False,
                  legend_name='case reported',
                  smooth_factor=0
                  )
mymap

#adding folium leaflet to make the map interactive
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
case = folium.features.GeoJson(
    world_df,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
                                            fields=['name','number'],
                                            aliases=['Country: ','Number of case: '],
                                            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                                          )
                              )
mymap.add_child(case)
mymap.keep_in_front(case)
folium.LayerControl().add_to(mymap)
mymap
