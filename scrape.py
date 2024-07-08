import re
import urllib.request
import modal

import os
slack_sdk_image = modal.Image.debian_slim().pip_install("slack-sdk")

stub = modal.Stub(name="link-scraper")

playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "apt-get update",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)


@stub.function(image=playwright_image)
async def get_links(cur_url: str):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(cur_url)
        links = await page.eval_on_selector_all("a[href]", "elements => elements.map(element => element.href)")
        await browser.close()

    print("Links", links)
    return links


@stub.function(image=slack_sdk_image, secret=modal.Secret.from_name("my-slack-secret"))
def bot_token_msg(channel, message):
    import slack_sdk
    client = slack_sdk.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    client.chat_postMessage(channel=channel, text=message)


@stub.function()
def daily_scrape():
    urls = ["http://modal.com", "http://github.com"]
    for links in get_links.map(urls):
        for link in links:
            bot_token_msg.remote("random", link)


@stub.local_entrypoint()
def main(url):
    url = "http://google.com"
    get_links.remote(url)
