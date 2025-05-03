import geocoder

# Get the current location based on your IP
g = geocoder.ip('me')

# Print the current latitude, longitude, and the address
if g.latlng:
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    address = g.address  # Get the address for the coordinates

    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Location: {address}")
else:
    print("Location not available")