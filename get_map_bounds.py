import pandas as pd
import folium

data = pd.read_csv("BP001_00100m.csv")

# Extract all latitude and longitude columns
longitude_columns = ["P1-Long", "P2-Long", "P3-Long", "P4-Long"]
latitude_columns = ["P1-Lat", "P2-Lat", "P3-Lat", "P4-Lat"]

all_longitudes = data[longitude_columns].values.flatten()
all_latitudes = data[latitude_columns].values.flatten()

# Compute the bounds
min_longitude = all_longitudes.min()
max_longitude = all_longitudes.max()
min_latitude = all_latitudes.min()
max_latitude = all_latitudes.max()

# Save the bounds
with open("bounding_box.txt", "w") as file:
    file.write(f"Bounding Box:\n")
    file.write(f"Minimum Longitude: {min_longitude}\n")
    file.write(f"Maximum Longitude: {max_longitude}\n")
    file.write(f"Minimum Latitude: {min_latitude}\n")
    file.write(f"Maximum Latitude: {max_latitude}\n")

# Create a map centered at the midpoint of the bounding box
map_center = [(min_latitude + max_latitude) / 2, (min_longitude + max_longitude) / 2]
m = folium.Map(location=map_center, zoom_start=13)

# Draw the bounding box
bounds = [
    [min_latitude, min_longitude],
    [min_latitude, max_longitude],
    [max_latitude, max_longitude],
    [max_latitude, min_longitude],
    [min_latitude, min_longitude],
]
folium.PolyLine(bounds, color="red", weight=6, opacity=0.8).add_to(m)

# Draw each quad mesh
for index, row in data.iterrows():
    quad = [
        [row["P1-Lat"], row["P1-Long"]],
        [row["P2-Lat"], row["P2-Long"]],
        [row["P3-Lat"], row["P3-Long"]],
        [row["P4-Lat"], row["P4-Long"]],
        [row["P1-Lat"], row["P1-Long"]],
    ]
    folium.PolyLine(quad, color="red", weight=1, opacity=0.8).add_to(m)

lod6_min_latitude = 34.602469074733456
lod6_max_latitude = 34.60281501212898
lod6_min_longitude = 135.46141994778742
lod6_max_longitude = 135.4621147708877

lod6 = [
    [lod6_min_latitude, lod6_min_longitude],  # Top-left
    [lod6_min_latitude, lod6_max_longitude],  # Top-right
    [lod6_max_latitude, lod6_max_longitude],  # Bottom-right
    [lod6_max_latitude, lod6_min_longitude],  # Bottom-left
    [lod6_min_latitude, lod6_min_longitude],  # Closing the quad
]

lod5_min_latitude = 34.6021274073895
lod5_max_latitude = 34.602816131799294
lod5_min_longitude = 135.46142088657962
lod5_max_longitude = 135.46211556461543

lod5 = [
    [lod5_min_latitude, lod5_min_longitude],  # Top-left
    [lod5_min_latitude, lod5_max_longitude],  # Top-right
    [lod5_max_latitude, lod5_max_longitude],  # Bottom-right
    [lod5_max_latitude, lod5_min_longitude],  # Bottom-left
    [lod5_min_latitude, lod5_min_longitude],  # Closing the quad
]

lod4_min_latitude = 34.601439961205905
lod4_max_latitude = 34.602818437197506
lod4_min_longitude = 135.4614008693341
lod4_max_longitude = 135.46282132507878

lod4 = [
    [lod4_min_latitude, lod4_min_longitude],  # Top-left
    [lod4_min_latitude, lod4_max_longitude],  # Top-right
    [lod4_max_latitude, lod4_max_longitude],  # Bottom-right
    [lod4_max_latitude, lod4_min_longitude],  # Bottom-left
    [lod4_min_latitude, lod4_min_longitude],  # Closing the quad
]

folium.PolyLine(lod6, color="blue", weight=6, opacity=0.8).add_to(m)
folium.PolyLine(lod5, color="green", weight=3, opacity=0.8).add_to(m)
folium.PolyLine(lod4, color="yellow", weight=2, opacity=0.8).add_to(m)

# Save the map to an HTML file for visualization
m.save("bounding_box_map.html")
