import streamlit as st
import exifread
import folium
from PIL import Image
from streamlit_folium import st_folium

# Function to extract GPS coordinates from the image
def get_exif_data(image):
    exif_data = {}
    with Image.open(image) as img:
        tags = exifread.process_file(image)
        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat = tags["GPS GPSLatitude"].values
            lon = tags["GPS GPSLongitude"].values
            lat_ref = tags["GPS GPSLatitudeRef"].values
            lon_ref = tags["GPS GPSLongitudeRef"].values
            exif_data['latitude'] = convert_to_degrees(lat, lat_ref)
            exif_data['longitude'] = convert_to_degrees(lon, lon_ref)
    return exif_data

# Convert EXIF GPS data to degrees
def convert_to_degrees(value, ref):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    degrees = d + (m / 60.0) + (s / 3600.0)
    if ref == 'S' or ref == 'W':
        degrees = -degrees
    return degrees

# Function to display map with multiple markers
def display_map(locations):
    map_center = [locations[0]['latitude'], locations[0]['longitude']]  # Center map at the first location
    map_ = folium.Map(location=map_center, zoom_start=5)

    for loc in locations:
        # Place a marker for each location without showing latitude and longitude in the UI
        folium.Marker(
            [loc['latitude'], loc['longitude']], 
            popup="Image Location",  # You can customize the popup text if needed
            tooltip="Click for more info",
            icon=folium.Icon(icon="cloud", prefix="fa", color="blue")  # Custom Icon
        ).add_to(map_)
    
    # Render the map with Streamlit
    st_folium(map_, width=700)

# Streamlit user interface
st.title("Multiple Image Upload with GPS Location Mapping")

# Allow multiple image upload
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    locations = []
    for uploaded_file in uploaded_files:
        # Extract EXIF data (GPS coordinates)
        exif_data = get_exif_data(uploaded_file)

        if exif_data:
            locations.append(exif_data)
        else:
            st.warning(f"No GPS data found in image: {uploaded_file.name}")

    if locations:
        st.success(f"Location data extracted for {len(locations)} images!")
        display_map(locations)
    else:
        st.warning("No images with valid GPS data were uploaded.")

