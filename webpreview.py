#!/usr/bin/env python

"""webpreview.py: It takes a screenshot of the websites passed through a file that contains URLs."""
__author__      = "Dbad"

import asyncio
import os
import sys
import time
import argparse
from urllib.parse import urlparse
from pyppeteer import launch

def get_max_length(lst):
    return len(max(lst, key=len))

async def screenshot(url, output_path):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await asyncio.sleep(2)
    await page.screenshot({'path': output_path})
    await browser.close()

async def generate_screenshots(url_file, output_dir):
    with open(url_file) as f:
        urls = [line.rstrip() for line in f]
    
    for url in urls:
        print("[+] Taking screenshot of " + url)
        path = urlparse(url).path.split("/")
        if get_max_length(path) > 0:          
            output_path = os.path.join(output_dir, urlparse(url).netloc+ "-".join(path) + '.png')
            await screenshot(url, output_path)
        else:
            output_path = os.path.join(output_dir, urlparse(url).netloc + '.png')
            await screenshot(url, output_path)

async def main():
    parser = argparse.ArgumentParser(description='Generate screenshots of websites.')
    parser.add_argument('url_file', type=str, help='path to file containing URLs')
    parser.add_argument('output_dir', type=str, help='path to directory to store screenshots')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    await generate_screenshots(args.url_file, args.output_dir)

if __name__ == '__main__':
    asyncio.run(main())
