import json
from facebook_scraper import get_posts

FILE = 'facebook_data.json'


def scrape_data():
    post_list = []
    for post in get_posts('amicale.deseleves', pages=3):
        print(post)
        cleaned_post = {
            "post_id": post["post_id"],
            "post_text": post["post_text"],
            "post_url": post["post_url"],
            "image": post["image"],
            "video": post["video"],
            "link": post["link"],
            "time": post["time"].timestamp(),
        }
        post_list.append(cleaned_post)
    return post_list


def write_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f)


def main():
    print("Fetching facebook data...")
    write_data(scrape_data())
    print('DONE')


main()
