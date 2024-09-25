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

# Function to display map with marker
def display_map(lat, lon):
    st.write(f"Latitude: {lat}, Longitude: {lon}")
    map_ = folium.Map(location=[lat, lon], zoom_start=15)

    # Use a custom FontAwesome icon for the marker
    folium.Marker(
        [lat, lon], 
        popup="Image Location",
        tooltip="Click for more info",
        icon=folium.Icon(icon="cloud", prefix="fa", color="blue")  # Custom Icon
    ).add_to(map_)
    
    # Render the map with Streamlit
    st_folium(map_, width=700)

# Streamlit user interface
st.title("Image Upload with GPS Location Mapping")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg"])

if uploaded_file:
    # Extract EXIF data (GPS coordinates)
    exif_data = get_exif_data(uploaded_file)

    if exif_data:
        # If GPS coordinates found, display map
        lat = exif_data['latitude']
        lon = exif_data['longitude']
        st.success("Location data extracted!")
        display_map(lat, lon)
    else:
        st.warning("No GPS data found in this image.")
