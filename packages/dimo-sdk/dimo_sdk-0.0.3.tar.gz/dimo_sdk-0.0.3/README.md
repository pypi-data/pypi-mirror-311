# dimo-sdk-python
python sdk for dimo，include hub operations


## install

```shell
pip install dimo-sdk
```

## usage

```python
from hub.client import Client

base_url = "http://52.76.75.134:8080"  # Replace with the actual base URL
client = Client(base_url)

# Example parameters
owner = "owner_name"
filename = "example_meme.jpg"
msg = "This is a test meme"

# Upload meme message
upload_response = client.upload_hub(owner, filename, msg)

# Example for downloading meme data
downloaded_data = client.download_hub_data(owner,filename)
if downloaded_data:
    with open('/tmp/downloaded_meme.jpg', 'wb') as f:
        f.write(downloaded_data)
    print("Download successful!")
else:
    print("Download failed!")
```