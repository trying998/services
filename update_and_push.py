import subprocess, sys, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

PAGE_DIR = Path(__file__).resolve().parent
INDEX_FILE = PAGE_DIR / 'index.html'
TEMPLATE = INDEX_FILE.read_text(encoding='utf-8')

URL_DIR = Path(r'C:\tmp\cloudflared')

SERVICES = [
    {'placeholder': 'STOCKBOT_URL',  'file': 'tunnel_8501_url.txt'},
    {'placeholder': 'AWARD_URL',     'file': 'tunnel_8080_url.txt'},
    {'placeholder': 'HR_URL',        'file': 'tunnel_8601_url.txt'},
    {'placeholder': 'FULLSTAFF_URL', 'file': 'tunnel_8603_url.txt'},
]


def read_url(filename: str) -> str:
    f = URL_DIR / filename
    if not f.exists():
        return 'https://trying998.github.io/services/'
    raw = f.read_bytes()
    return raw.decode('utf-8-sig').strip().replace('﻿', '')


def main():
    html = TEMPLATE
    for svc in SERVICES:
        url = read_url(svc['file'])
        html = html.replace(svc['placeholder'], url)

    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M')
    html = html.replace('UPDATED_AT', now)

    INDEX_FILE.write_text(html, encoding='utf-8')

    os.chdir(PAGE_DIR)

    subprocess.run(['git', 'add', 'index.html'], check=True, capture_output=True)

    result = subprocess.run(
        ['git', 'commit', '-m', f'Auto-update URLs {now}'],
        capture_output=True, text=True
    )
    if 'nothing to commit' in result.stdout + result.stderr:
        print('No changes to push')
        return

    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print(f'Pushed at {now}')

    for svc in SERVICES:
        url = read_url(svc['file'])
        print(f'  {svc["placeholder"]}: {url}')


if __name__ == '__main__':
    main()
