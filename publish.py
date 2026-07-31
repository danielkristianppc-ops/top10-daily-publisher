import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error
 
IG_USER_ID = "27702607289433823"
ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
GRAPH = "https://graph.instagram.com/v21.0"
 
# Content feed: a small JSON blob (day number -> {images, caption}) that gets
# refilled automatically by a weekly content-generation job. This script never
# needs to change again — new weeks just add more keys to this feed.
MANIFEST_URL = "https://jsonblob.com/api/jsonBlob/019fb93a-19b3-7073-ae8a-dc730ca9fa1a"
 
 
def http_get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())
 
 
def api_post(path, params):
    url = f"{GRAPH}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} calling {path}: {body}") from None
 
 
def main():
    with open("state.json") as f:
        state = json.load(f)
 
    day = state["next_day"]
 
    manifest = http_get_json(MANIFEST_URL)
    cfg = manifest.get(str(day))
 
    if cfg is None:
        print(
            f"No content queued yet for day {day}. "
            "Nothing to publish today — the weekly content job hasn't caught up. "
            "Not advancing the counter; will retry tomorrow."
        )
        return
 
    caption = cfg["caption"]
 
    print(f"Publishing day {day}")
 
    child_ids = []
    for image_url in cfg["images"]:
        res = api_post(
            f"{IG_USER_ID}/media",
            {
                "image_url": image_url,
                "is_carousel_item": "true",
                "access_token": ACCESS_TOKEN,
            },
        )
        if "id" not in res:
            raise RuntimeError(f"Failed to create child container for {image_url}: {res}")
        child_ids.append(res["id"])
        print(f"  created child container: {res['id']}")
        time.sleep(1)
 
    parent = api_post(
        f"{IG_USER_ID}/media",
        {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
            "access_token": ACCESS_TOKEN,
        },
    )
    if "id" not in parent:
        raise RuntimeError(f"Failed to create carousel parent: {parent}")
    print(f"  created carousel parent: {parent['id']}")
 
    time.sleep(5)
 
    publish = api_post(
        f"{IG_USER_ID}/media_publish",
        {
            "creation_id": parent["id"],
            "access_token": ACCESS_TOKEN,
        },
    )
    if "id" not in publish:
        raise RuntimeError(f"Failed to publish: {publish}")
 
    print(f"Published day {day} as media id {publish['id']}")
 
    state["next_day"] = day + 1
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
 
 
if __name__ == "__main__":
    main()
