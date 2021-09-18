import json
import facebook_scraper

FILE = 'facebook_data.json'

PAGES = ["amicale.deseleves", "campus.insat"]


def scrape_data(page):
    post_list = []
    for post in facebook_scraper.get_posts(page, pages=4):
        print(post)
        cleaned_post = {
            "id": post["post_id"],
            "message": post["post_text"],
            "url": post["post_url"],
            "image": post["image"],
            "images": post["images"],
            "video": post["video"],
            "link": post["link"],
            "time": post["time"].timestamp(),
            "page_id": page,
        }
        post_list.append(cleaned_post)
    return post_list


def get_all_data():
    data = {}
    for page in PAGES:
        print("   -> " + page)
        # On ne parse que campus car l'amicale ne marche pas
        if page != "amicale.deseleves":
            data[page] = scrape_data(page)
        else:
            data[page] = []
    return data


def write_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f)


def main():
    print("Fetching facebook data...")
    write_data(get_all_data())
    print('DONE')


main()
