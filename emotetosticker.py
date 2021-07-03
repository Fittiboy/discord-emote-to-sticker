import argparse
import requests
import re


def get_value(text, name):
    token_search_str = f"value=\"[a-z0-9-.]+\" name=\"{name}\""
    token_match = re.search(token_search_str, text, re.I)
    token = token_match.group().split('"')[1]
    return token


def get_action(text):
    search_str = "action=\".+\" method=\"POST\""
    match = re.search(search_str, text, re.I)
    action = match.group().split('"')[1]
    return action


def get_apng_url(response):
    search_str = "<a class=\"save\" href=\"" + \
                      "https://s[0-9]{1,2}.ezgif[./a-z0-9-]+(?!gif)png\""
    match = re.search(search_str, response.text, re.I)
    apng = match.group().split('"')[3]
    return apng


def convert_to_apng(emote_url):
    url_base = "https://ezgif.com/gif-to-apng"
    params = {
        "url": emote_url,
    }
    conv_r = requests.get(url_base, params)

    file = get_value(conv_r.text, "file")
    token = get_value(conv_r.text, "token")
    action = get_action(conv_r.text)

    data = {
        "token": token,
        "file": file
    }

    response = requests.post(url=action, data=data)
    return get_apng_url(response)


def resize_apng(emote_url):
    url_base = "https://ezgif.com/resize"
    params = {
        "url": emote_url,
    }
    resize_r = requests.get(url_base, params)

    file = get_value(resize_r.text, "file")
    token = get_value(resize_r.text, "token")
    old_width = int(get_value(resize_r.text, "old_width"))
    old_height = int(get_value(resize_r.text, "old_height"))
    height = 320
    width = 320
    action = get_action(resize_r.text)
    percentage = max(height / old_height, width / old_width) * 100

    data = {
        "token": token,
        "file": file,
        "old_width": old_width,
        "old_height": old_height,
        "width": width,
        "height": height,
        "percentage": percentage
    }

    response = requests.post(url=action, data=data)
    return get_apng_url(response)


def main():
    parser = argparse.ArgumentParser(prog="Emote To Sticker")
    parser.add_argument("emote_url",
                        help="The URL you get when you right-click "
                        "an emote in a Discord message and hit the "
                        "'Copy Link' option",
                        metavar="Emote URL",
                        type=str)
    args = parser.parse_args()
    apng = convert_to_apng(args.emote_url)
    apng = resize_apng(apng)
    return apng


if __name__ == "__main__":
    print(main())
