#!/usr/bin/env python3

import argparse
import requests
import os
import io

import twitch
from PIL import Image


client_id = os.environ['TWITCH_CLIENT_ID']
client_secret = os.environ['TWITCH_SECRET']

margin = 24
size = 512


def main(username: str, out_dir: str):
    output_dir = out_dir + '/' + username.lower()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    helix = twitch.Helix(client_id, client_secret)

    # Get user ID
    user = helix.user(username)

    # Get emote list
    params = dict()
    params['broadcaster_id'] = user.id
    emotes = helix.api.get('chat/emotes', params)['data']

    # Download emotes
    for emote in emotes:
        print("downloading " + emote['name'])
        images = emote['images']
        if 'url_4x' in images:
            emote_path = output_dir + '/' + emote['name'] + '.png'
            if not os.path.exists(emote_path):
                data = requests.get(images['url_4x'], allow_redirects=True)

                with open(emote_path, 'wb') as f:
                    with Image.open(io.BytesIO(data.content)) as im:
                        s = size - margin * 2
                        add_margin(im.resize((s, s)), margin).save(f)


def add_margin(pil_img, margin):
    width, height = pil_img.size
    new_width = width + margin * 2
    new_height = height + margin * 2
    result = Image.new("RGBA", (new_width, new_height))
    result.putalpha(0)
    result.paste(pil_img, (margin, margin))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download Twitch emotes to be used as Signal stickers.')

    parser.add_argument('username', help='Twitch username')
    parser.add_argument('-o', dest='out_dir', default='./out',
                        help='base output directory')

    args = parser.parse_args()
    main(username=args.username, out_dir=args.out_dir)
