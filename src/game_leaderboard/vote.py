import logging
from pathlib import Path

import requests

logging.basicConfig(level=logging.DEBUG)

TOKENS_FILE = Path(__file__).parent / "tokens.txt"


def read_tokens() -> list[str]:
    if not TOKENS_FILE.exists():
        return []
    return [
        line.strip()
        for line in TOKENS_FILE.read_text().splitlines()
        if line.strip()
    ]


def game_vote(auth, universe_id=324740367, vote=1):
    logging.debug(f"Voting with auth: {auth}, universe_id: {universe_id}, vote: {vote}")
    url = "https://voidstrapp.pages.dev/api/gamevote"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth}",
        "Referer": f"https://voidstrapp.pages.dev/pages/place?id={universe_id}&name=parkour-reborn",
        "Origin": "https://voidstrapp.pages.dev",
    }

    payload = {
        "universeId": universe_id,
        "vote": vote
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text


def main():
    tokens = read_tokens()

    if not tokens:
        logging.error(f"No tokens found in {TOKENS_FILE}")
        return

    logging.info(f"Found {len(tokens)} token(s) in {TOKENS_FILE}")

    for i, token in enumerate(tokens, start=1):
        logging.info(f"Voting with token {i}/{len(tokens)}")
        result = game_vote(token)
        logging.info(f"Vote result: {result}")

    logging.info("Completed all votes")


if __name__ == "__main__":
    main()
