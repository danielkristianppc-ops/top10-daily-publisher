import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error

IG_USER_ID = "27702607289433823"
ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
GRAPH = "https://graph.instagram.com/v21.0"

DAYS = {
    2: dict(
        images=[
            "https://i.postimg.cc/13rTVffP/slide-01-hook.png",
            "https://i.postimg.cc/52SGQ66j/slide-02-fact1.png",
            "https://i.postimg.cc/jS49nLLD/slide-03-fact2.png",
            "https://i.postimg.cc/rwNbRKKK/slide-04-fact3.png",
            "https://i.postimg.cc/6pfS4yy4/slide-05-fact4.png",
            "https://i.postimg.cc/XYkhBppf/slide-06-fact5.png",
            "https://i.postimg.cc/GmxNTHHP/slide-07-fact6.png",
            "https://i.postimg.cc/rpyH1Mr0/slide-08-fact7.png",
            "https://i.postimg.cc/FKF6yNLf/slide-09-fact8.png",
            "https://i.postimg.cc/yN6GmsZ3/slide-10-fact9-10.png",
        ],
        caption=(
            "#3 explains a lot of group chats. Save this list, you'll want to "
            "reference it later. Tag a friend who needs #7. Follow for a new "
            "Top 10 every day.\n\n#top10 #psychologyfacts #humanbehavior #mindset"
        ),
    ),
    3: dict(
        images=[
            "https://i.postimg.cc/hGGCJsk0/slide-01-hook.png",
            "https://i.postimg.cc/TPPky0z7/slide-02-fact1.png",
            "https://i.postimg.cc/VNN7SgxK/slide-03-fact2.png",
            "https://i.postimg.cc/1zzWgBkJ/slide-04-fact3.png",
            "https://i.postimg.cc/LssyqDcy/slide-05-fact4.png",
            "https://i.postimg.cc/TPPky0zB/slide-06-fact5.png",
            "https://i.postimg.cc/k55jVs0k/slide-07-fact6.png",
            "https://i.postimg.cc/R00P3Grr/slide-08-fact7.png",
            "https://i.postimg.cc/CKKvZJyp/slide-09-fact8.png",
            "https://i.postimg.cc/Pqq6LKGH/slide-10-fact9-10.png",
        ],
        caption=(
            "#1 gets people every time. Save this for your next trivia night — "
            "which one did you not believe? Follow for a new Top 10 every day.\n\n"
            "#top10 #historyfacts #didyouknow #truestory"
        ),
    ),
    4: dict(
        images=[
            "https://i.postimg.cc/s2ndNwdM/slide-01-hook.png",
            "https://i.postimg.cc/hGCW5pW9/slide-02-fact1.png",
            "https://i.postimg.cc/wBW8G08D/slide-03-fact2.png",
            "https://i.postimg.cc/MGs2Fd2V/slide-04-fact3.png",
            "https://i.postimg.cc/25HRK2RQ/slide-05-fact4.png",
            "https://i.postimg.cc/N0Nqzpq4/slide-06-fact5.png",
            "https://i.postimg.cc/rphXPQXj/slide-07-fact6.png",
            "https://i.postimg.cc/CKvTQmTv/slide-08-fact7.png",
            "https://i.postimg.cc/k5j3pf3Y/slide-09-fact8.png",
            "https://i.postimg.cc/85jQQMNB/slide-10-fact9-10.png",
        ],
        caption=(
            "Save this before your next movie night — you'll be the one pointing "
            "out #1 and #2. Which easter egg did you already know about? Follow "
            "for a new Top 10 every day.\n\n#top10 #movietrivia #easteregg #didyouknow"
        ),
    ),
    5: dict(
        images=[
            "https://i.postimg.cc/VLyypJpP/slide-01-hook.png",
            "https://i.postimg.cc/02ggFzFP/slide-02-fact1.png",
            "https://i.postimg.cc/PrmGjts9/slide-03-fact2.png",
            "https://i.postimg.cc/MKykSW24/slide-04-fact3.png",
            "https://i.postimg.cc/zXmm6y6q/slide-05-fact4.png",
            "https://i.postimg.cc/5NwcVxWd/slide-06-fact5.png",
            "https://i.postimg.cc/ZKrkSTzh/slide-07-fact6.png",
            "https://i.postimg.cc/zXnmrJYN/slide-08-fact7.png",
            "https://i.postimg.cc/15pxQ91s/slide-09-fact8.png",
            "https://i.postimg.cc/3JgMTKQ3/slide-10-fact9-10.png",
        ],
        caption=(
            "#3 is the wholesome one you didn't need today. Save this list — tag "
            "someone who loves animal facts. Follow for a new Top 10 every day.\n\n"
            "#top10 #animalfacts #wildlife #didyouknow"
        ),
    ),
    6: dict(
        images=[
            "https://i.postimg.cc/nLhNBBj9/slide-01-hook.png",
            "https://i.postimg.cc/W41xggFg/slide-02-fact1.png",
            "https://i.postimg.cc/Zq5XppB6/slide-03-fact2.png",
            "https://i.postimg.cc/DzwRLLJQ/slide-04-fact3.png",
            "https://i.postimg.cc/Pq50YYpm/slide-05-fact4.png",
            "https://i.postimg.cc/TPNF91gy/slide-06-fact5.png",
            "https://i.postimg.cc/pdc4Zrz5/slide-07-fact6.png",
            "https://i.postimg.cc/q7DSLqyK/slide-08-fact7.png",
            "https://i.postimg.cc/VNZpRvnC/slide-09-fact8.png",
            "https://i.postimg.cc/9fgKp0Zy/slide-10-fact9-10.png",
        ],
        caption=(
            "#6 is a little unsettling but very true. Save this — you'll want to "
            "fact-drop #1 at dinner. Follow for a new Top 10 every day.\n\n"
            "#top10 #bodyfacts #didyouknow #humanbody"
        ),
    ),
    7: dict(
        images=[
            "https://i.postimg.cc/L6F7vrYc/slide-01-hook.png",
            "https://i.postimg.cc/CLptJWnp/slide-02-fact1.png",
            "https://i.postimg.cc/jdY9vGnT/slide-03-fact2.png",
            "https://i.postimg.cc/7YrcXpJk/slide-04-fact3.png",
            "https://i.postimg.cc/7YrcXpJy/slide-05-fact4.png",
            "https://i.postimg.cc/m2WqV01Z/slide-06-fact5.png",
            "https://i.postimg.cc/28NJTPL8/slide-07-fact6.png",
            "https://i.postimg.cc/Dy3D5t4Z/slide-08-fact7.png",
            "https://i.postimg.cc/4NRMwrH3/slide-09-fact8.png",
            "https://i.postimg.cc/Fsb66D0r/slide-10-fact9-10.png",
        ],
        caption=(
            "#2 is the one everyone already half-knows but loves hearing again. "
            "Save this for your next 'useless facts' moment. Follow for a new "
            "Top 10 every day.\n\n#top10 #inventions #didyouknow #history"
        ),
    ),
}


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
    if day > 7:
        print("All 7 days already published. Nothing scheduled to do.")
        return

    cfg = DAYS[day]
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
