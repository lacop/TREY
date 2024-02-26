# Scrape all the comic info from reddit.

from dotenv import load_dotenv
import json
import os
import praw
import re
import tqdm

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent='trey',
)

# Thanks u/fyxr
INDEX_URL = 'https://www.reddit.com/r/comics/comments/1avuap5/the_trey_saga/'
index_raw = reddit.submission(url=INDEX_URL).selftext
comid_ids = re.findall(r'\[[^\]]+\]\(/r/comics/comments/([^/]+).*\)', index_raw)
print(f'{len(comid_ids)=}')

def largest_url(media):
    return max(media['p'], key=lambda x: x['y'])['u']

comics = []
for cid in tqdm.tqdm(comid_ids):
    submission = reddit.submission(id=cid)
    if not hasattr(submission, 'gallery_data'):
        continue
    comics.append({
        'id': submission.id,
        'title': submission.title,
        'url': submission.url,
        'author': submission.author.name,
        'score': submission.score,
        'created_utc': submission.created_utc,
        'frames': [
            largest_url(submission.media_metadata[item['media_id']])
            for item in submission.gallery_data['items']
        ]
    })
print(f'{len(comics)=}')

with open('comics.json', 'w') as f:
    json.dump(comics, f, indent=2)