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
            main {
                height: 100vh;
                width: 100vw;
                display: flex;
                flex-direction: column;
                gap: 1rem;
                overflow-y: scroll;
                scroll-snap-type: y mandatory;
                scroll-padding: 1rem;
            }

            .comic {
                scroll-snap-align: start;
                width: 100%;
                min-height: 85vh;
            }
            
            .images {
                display: flex;
                flex-direction: row;
                gap: 1rem;
                padding-top: 3rem;
                overflow-x: scroll;
                /*scroll-snap-type: x proximity;
                scroll-padding: 0 3vw;*/
            }

            .topbar {
                min-height: 5vh;
                padding-left: 10vw;
                font-size: 3rem;
            }

            h1 {
                padding-left: 3rem;
                font-size: 4rem;
            }

            h2 {
                font-size: 4rem;
                margin-bottom: 1rem;
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
        <main>
'''

for i, comic in enumerate(comics):
    title = comic['title'].strip('.').strip()
    
    time_after = ', the one that started it all'
    if comic['created_utc'] > first:
        time_after = f''', {time_ago(comic['created_utc'])} after TREY'''

    output += f'''
            <div class="comic">
                <div class="topbar">
                    <h2>
                        <a href="{comic['url']}">{title}</a>
                        by {comic['author']}
                    </h2>
                    #{i+1} / {len(comics)}{time_after}.<br />
                    {humanize.intcomma(comic['score'])} points, {len(comic['frames'])} panels.
                </div>
                <div class="images">
    '''
    for frame in comic['frames']:
        output += f'''
                    <img src="{frame}" alt="a comic panel" />
        '''

    output += '''
                </div>
            </div>
    '''

output += '''
        </main>
    </body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(output)
