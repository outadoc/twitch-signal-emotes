#!/usr/bin/env python3

import argparse
import requests
import os
import io

import twitch
from PIL import Image
from PIL import ImageSequence

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_SECRET"]

TARGET_MARGIN = 32
TARGET_SIZE = 512


def main(username: str, out_dir: str):
    output_dir_raw = f"{out_dir}/{username.lower()}/raw"
    output_dir_processed = f"{out_dir}/{username.lower()}/processed"

    if not os.path.exists(output_dir_raw):
        os.makedirs(output_dir_raw)

    if not os.path.exists(output_dir_processed):
        os.makedirs(output_dir_processed)

    helix = twitch.Helix(client_id, client_secret)

    # Get user ID
    user = helix.user(username)

    # Get emote list
    params = dict()
    params["broadcaster_id"] = user.id
    emotes = helix.api.get("chat/emotes", params)["data"]

    # Example emote format:
    # {
    #  "id": "emotesv2_7ebfa7a173b549e3b906aef54d51c322",
    #  "name": "htyKnuk",
    #  "images": {
    #    "url_1x": "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_7ebfa7a173b549e3b906aef54d51c322/static/light/1.0",
    #    "url_2x": "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_7ebfa7a173b549e3b906aef54d51c322/static/light/2.0",
    #    "url_4x": "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_7ebfa7a173b549e3b906aef54d51c322/static/light/3.0"
    #  },
    #  "tier": "1000",
    #  "emote_type": "subscriptions",
    #  "emote_set_id": "418849315",
    #  "format": ["static", "animated"],
    #  "scale": ["1.0", "2.0", "3.0"],
    #  "theme_mode": ["light", "dark"]
    # }

    # Download emotes
    for i, emote in enumerate(emotes):
        is_animated = "animated" in emote["format"]

        format = "animated" if is_animated else "static"
        ext = "gif" if is_animated else "png"
        url = f"https://static-cdn.jtvnw.net/emoticons/v2/{emote['id']}/{format}/light/3.0"

        raw_path = f"{output_dir_raw}/{emote['name']}.{ext}"

        print(f"Getting {i+1}/{len(emotes)}: {emote['name']} ({format})")

        if not os.path.exists(raw_path):
            print(f"  Downloading {url} -> {raw_path}")
            data = requests.get(url, allow_redirects=True)

            with open(raw_path, "wb") as f:
                # Download to file
                f.write(data.content)

            print(f"  Saved to {raw_path}")

        image_format = "apng" if is_animated else "png"
        processed_path = f"{output_dir_processed}/{emote['name']}.{image_format}"
        print(f"  Processing {raw_path} -> {processed_path}")

        # Resize and add margin using ImageMagick
        emote_size = TARGET_SIZE - TARGET_MARGIN * 2

        os.system(
            f"convert {raw_path} -format {image_format} -background transparent -gravity center -scale {emote_size}x{emote_size} -extent {TARGET_SIZE}x{TARGET_SIZE} {processed_path}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Twitch emotes to be used as Signal stickers."
    )

    parser.add_argument("username", help="Twitch username")
    parser.add_argument(
        "-o", dest="out_dir", default="./out", help="base output directory"
    )

    args = parser.parse_args()
    main(username=args.username, out_dir=args.out_dir)
