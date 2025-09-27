from imagegen import write_text
import requests
import time

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
IG_USER_ID = 'YOUR_IG_USER_ID'  # Not username — this is numeric
IMAGE_URLS = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg"
]

def create_post():
    imageoutput = write_text()


    for image in imageoutput:
        





# Step 1: Upload images and get container IDs
container_ids = []

for url in IMAGE_URLS:
    upload_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        'image_url': url,
        'is_carousel_item': 'true',
        'access_token': ACCESS_TOKEN
    }
    res = requests.post(upload_url, data=payload)
    res_json = res.json()

    if 'id' in res_json:
        container_ids.append(res_json['id'])
        print(f"Uploaded: {url}")
    else:
        print(f"Failed to upload: {url} - {res_json}")

# Wait a few seconds to ensure containers are ready
time.sleep(5)

# Step 2: Create carousel container
carousel_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
children = ",".join(container_ids)
carousel_payload = {
    'media_type': 'CAROUSEL',
    'children': children,
    'caption': 'This is a carousel post from the API!',
    'access_token': ACCESS_TOKEN
}
carousel_res = requests.post(carousel_url, data=carousel_payload)
carousel_res_json = carousel_res.json()

if 'id' not in carousel_res_json:
    print(f"Failed to create carousel: {carousel_res_json}")
    exit()

carousel_container_id = carousel_res_json['id']
print(f"Carousel container created: {carousel_container_id}")

# Step 3: Publish the carousel
publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
publish_payload = {
    'creation_id': carousel_container_id,
    'access_token': ACCESS_TOKEN
}
publish_res = requests.post(publish_url, data=publish_payload)
publish_res_json = publish_res.json()

if 'id' in publish_res_json:
    print(f"Post published! ID: {publish_res_json['id']}")
else:
    print(f"Failed to publish post: {publish_res_json}")
