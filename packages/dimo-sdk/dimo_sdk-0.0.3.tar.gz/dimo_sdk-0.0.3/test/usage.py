from hub.client import Client

base_url = "http://localhost:8080"  # Replace with the actual base URL
client = Client(base_url)

# Example parameters
owner = "owner_name"
filename = "example_meme1.jpg"
msg = "This is a test meme"

# Upload meme message
upload_response = client.upload_hub(owner, filename, msg)

# Example for uploading actual data (e.g., image file)
with open('test/client.py', 'rb') as f:
    image_data = f.read()

dataname = "data_meme1.jpg"
upload_data_response = client.upload_hub_data(owner, dataname, image_data)

# Example for downloading meme data
downloaded_data = client.download_hub_data(owner,filename)
if downloaded_data:
    with open('/tmp/downloaded_meme.jpg', 'wb') as f:
        f.write(downloaded_data)
    print("Download successful!")
else:
    print("Download failed!")
