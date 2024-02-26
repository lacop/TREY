import datetime
import humanize
import json

with open('comics.json') as f:
    raw_comics = json.load(f)
print(f'{len(raw_comics)=}')

comics = []
ids = set()
for comic in sorted(raw_comics, key=lambda x: x['created_utc']):
    if comic['id'] in ids:
        continue
    ids.add(comic['id'])
    comics.append(comic)
print(f'{len(comics)=}')
print(f'{sum(len(c["frames"]) for c in comics)=}')

first = comics[0]['created_utc']
def time_ago(created_utc):
    dt = datetime.timedelta(seconds=created_utc - first)
    return humanize.naturaldelta(dt)

output = '''
<!DOCTYPE html>
<html>
<head>
    <title>TREY</title>
    <style>
        #comics {
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            gap: 1em;
            overflow-y: scroll;
            scroll-snap-type: y mandatory;
            scroll-padding: 1em;
        }

        .comic {
            scroll-snap-align: start;
            width: 100%;
            min-height: 85vh;
        }

        .comic:first-child {
            padding-top: 1em;
        }
        
        .images {
            display: flex;
            flex-direction: row;
            gap: 1em;
            overflow-x: scroll;
            /*scroll-snap-type: x proximity;
            scroll-padding: 0 3vw;*/
            padding: auto;
        }

        .topbar {
            min-height: 5vh;
            font-size: 150%;    
        }

        .title {
            font-size: 150%;
        }

        img {
            scroll-snap-align: start;
            min-width: 70vw;
            max-height: 80vh;
        }

        img:first-child {
            padding-left: 10vw;
        }
    </style>
</head>
<body>
    <div id="comics">
'''

for i, comic in enumerate(comics):
    title = comic['title'].strip('.').strip()
    
    time_after = ', the one that started it all'
    if comic['created_utc'] > first:
        time_after = f''', {time_ago(comic['created_utc'])} after TREY'''

    output += f'''
    <div class="comic">
        <div class="topbar">
            <div class="title">
                <strong><a href="{comic['url']}">{title}</a></strong>
                by {comic['author']}
            </div>
            #{i+1} / {len(comics)}{time_after}.<br>
            {humanize.intcomma(comic['score'])} points, {len(comic['frames'])} panels.
        </div>
        <div class="images">
    '''
    for frame in comic['frames']:
        output += f'<img src="{frame}">\n'

    output += '''
        </div>
    </div>
    '''

output += '''
</div>
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(output)