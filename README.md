# Streamlit Image GPS Mapper

This is a Streamlit application that allows users to upload images and automatically extract and map their location (GPS) data if embedded in the image metadata.

## Features

- Upload an image (.jpg or .jpeg) with embedded GPS EXIF data.
- Automatically extract the GPS coordinates from the image.
- Display the image's location on an interactive map.

## How to Use

1. **Upload an Image**: Click the upload button and select a `.jpg` or `.jpeg` image.
2. **View the Map**: If the image contains GPS metadata, the app will show the location on an interactive map.
3. **No GPS Data?**: If no GPS data is found in the image, you'll see a warning message.

## Installation

To run this application locally:

1. Clone this repository:

   ```bash
   git clone https://github.com/Iamkrmayank/Image_Location.git
   
cd Image-Location

pip install -r requirements.txt

streamlit run app.py


