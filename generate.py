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
        <title>TREY Comic Book</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
            header {
                height: 4.5rem;
                width: 100%;
                position: fixed;
                top: 0;
                padding-left: 1rem;
                background-color: white;
                border-bottom: 0.25rem dashed black;

                h1 {
                    margin-bottom: 0;
                    font-size: 2rem;
                }
            }

            main {
                height: 100vh;
                width: 100vw;
                display: flex;
                flex-direction: column;
                gap: 1rem;
                overflow-y: scroll;
                scroll-snap-type: y mandatory;
                scroll-padding: 1rem;

                .comic {
                    scroll-snap-align: start;
                    scroll-margin-top: 4.5rem;
                    width: 100%;
                    min-height: 85vh;

                    .topbar {
                        min-height: 5vh;
                        padding-left: 10vw;
                        font-size: 1rem;

                        h2 {
                            font-size: 1.5rem;
                            margin-bottom: 0.5rem;
                        }
                    }

                    .images {
                        display: flex;
                        flex-direction: row;
                        gap: 1rem;
                        padding-top: 1rem;
                        overflow-x: scroll;

                        img {
                            scroll-snap-align: start;
                            min-width: 70vw;
                            max-height: 80vh;
                        }

                        img:first-child {
                            padding-left: 10vw;
                        }
                    }
                }

                .comic:first-child {
                    margin-top: 4rem;
                }
            }

            footer {
                position: sticky;
                bottom: 0;
                padding: 1rem;
                background-color: white;
                border-top: 0.25rem dashed black;
            }

            /* MD */
            @media (768px <= width) {
                main {
                    .comic {
                        min-height: unset;

                        .topbar {
                            min-height: unset;
                            padding-left: 4rem;
                            font-size: 1.5rem;

                            h2 {
                                font-size: 2rem;
                            }
                        }

                        .images {
                            img {
                                min-width: unset;
                                max-height: 30rem;
                            }

                            img:first-child {
                                padding-left: 4rem;
                            }
                        }
                    }
                }
            }

            /* LG */
            @media (992px <= width) {
                header,
                footer {
                    padding-left: 4rem;
                }

                main {
                    .comic {
                        .topbar {
                            padding-left: 8rem;
                        }

                        .images {
                            img:first-child {
                                padding-left: 8rem;
                            }
                        }
                    }
                }
            }

            /* XL */
            @media (1200px <= width) {
                header,
                footer {
                    padding-left: 8rem;
                }

                main {
                    .comic {
                        .topbar {
                            padding-left: 16rem;
                        }

                        .images {
                            img:first-child {
                                padding-left: 16rem;
                            }
                        }
                    }
                }
            }

            @media (prefers-color-scheme: dark) {
                html {
                    color: whitesmoke;
                    background-color: #141414;

                    header,
                    footer {
                        background-color: #141414;
                        border-color: whitesmoke;
                    }

                    a {
                        color: mediumblue;
                    }

                    a:visited {
                        color: rebeccapurple;
                    }

                    a:active {
                        color: firebrick;
                    }
                }
            }
        </style>
    </head>
    <body>
        <header>
            <h1>TREY Comic Book</h1>
        </header>
        <main>
'''

for i, comic in enumerate(comics):
    title = comic['title'].strip('.').strip()
    
    time_after = ', the one that started it all'
    if comic['created_utc'] > first:
        time_after = f''', {time_ago(comic['created_utc'])} after TREY'''

    output += f'''
            <div class="comic" id="{i+1}">
                <div class="topbar">
                    <h2>
                        <a href="https://old.reddit.com/{comic['id']}">{title}</a>
                        by {comic['author']}
                    </h2>
                    #{i+1} / {len(comics)}{time_after}.<br />
                    {humanize.intcomma(comic['score'])} points | {len(comic['frames'])} panels | <a href="#{i+1}">perm</a>
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
        <footer>
'''

for i, _ in enumerate(comics):
    increased_i = i + 1
    formatted_i = f"{increased_i:02}"

    output += f'''
            [<a href="#{increased_i}">#{formatted_i}</a>]
    '''


output += '''
        </footer>
    </body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(output)
