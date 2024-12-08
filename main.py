import os
import random

import tweepy


def main():
    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_KEY_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )
    segment_groups = []
    group = []
    ignore = False
    with open("./lyrics.txt") as lyricsfile:
        for segment in lyricsfile.read().split("\n\n"):
            seg = segment.strip()
            if seg.startswith("===="):
                if group:
                    if not ignore:
                        segment_groups.append(group)
                    group = []
                ignore = ("/" in seg)
            elif seg:
                group.append(seg)
        if group and not ignore:
            segment_groups.append(group)

    print(f"Found {len(segment_groups)} songs")

    trials = 3
    while trials > 0:
        gidx = random.randint(0, len(segment_groups) - 1)
        group = segment_groups[gidx]
        idx = random.randint(0, len(group) - 1)
        try:
            client.create_tweet(text=group[idx])
            print(group[idx])
            return
        except tweepy.errors.Forbidden as e:
            print('lyrics upload fail (forbidden)')
            trials -= 1
        except tweepy.errors.BadRequest as e:
            print('lyrics upload fail (bad request)')
            trials -= 1
        except tweepy.errors.TooManyRequests as e:
            resp = e.response
            limit_reset = resp.headers.get('x-rate-limit-reset', 'UNKNOWN')
            print(f'rate limit exceeded: resets in {limit_reset} seconds')
            return

    print('lyrics upload failed after 3 retries')


if __name__ == '__main__':
    main()

