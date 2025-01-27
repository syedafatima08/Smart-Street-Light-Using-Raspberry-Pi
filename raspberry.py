from picamera import PiCamera
from time import sleep
import requests
import datetime

# Configure this with your server's address
url = 'http://192.168.146.91:5000/upload'

camera = PiCamera()

def capture_and_send():
    # Generate a timestamped filename for each image
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
    
    # Take a picture
    camera.capture(filename)
    
    # Prepare the file to send
    files = {'file': (filename, open(filename, 'rb'))}
    
    # Send the POST request with the file
    response = requests.post(url, files=files)
    
    # Optionally, handle the response
    print(response.text)
    
    # Clean up by removing the image file if not needed locally
    # os.remove(filename)

# Take a picture and send it every 5 minutes
while True:
    capture_and_send()
    sleep(300)  # Sleep for 5 minutes