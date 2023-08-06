# Vedro Playwright Plugin

[![PyPI](https://img.shields.io/pypi/v/vedro-playwright.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-playwright?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-playwright.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)

[Vedro](https://vedro.io/) + [playwright](https://playwright.dev/python/)

(forked from [vedro-pyppeteer](https://github.com/nikitanovosibirsk/vedro-pyppeteer))

## Installation

### 1. Install package

```shell
$ pip3 install vedro-playwright
$ playwright install
```

### 2. Enable plugin

```python
# ./vedro.cfg.py
import vedro
import vedro_playwright as playwright

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class Playwright(playwright.Playwright):
            enabled = True
```

## Usage

```python
# ./scenarios/reset_password.py
import vedro
from vedro_playwright import BrowserEngine as Browser
from vedro_playwright import opened_firefox_page, opened_chromium_page, opened_webkit_page

class Scenario(vedro.Scenario):
    subject = "reset password (via {browser})"

    @vedro.params(Browser.CHROMIUM, opened_chromium_page)
    @vedro.params(Browser.FIREFOX, opened_firefox_page)
    @vedro.params(Browser.WEBKIT, opened_webkit_page)
    def __init__(self, browser, opened_page):
        self.opened_page = opened_page

    async def given_opened_app(self):
        self.page = await self.opened_page()
        await self.page.goto("http://localhost:8080/reset")

    async def given_filled_email(self):
        form_email = self.page.locator("#form-email")
        await form_email.type("user@email")

    async def when_user_submits_form(self):
        await self.page.click("#form-submit")

    async def then_it_should_redirect_to_root_page(self):
        pathname = await self.page.evaluate("window.location.pathname")
        assert pathname == "/"
```

```shell
$ vedro run --playwright-screenshots=on_fail
```

## Documentation

### Plugin

`--playwright-screenshots=<mode>`

| Mode        | Description                                        |
| ----------- | -------------------------------------------------- |
| every_step  | Save screenshots for every step                    |
| only_failed | Save screenshots only for failed steps             |
| on_fail     | Save screenshots for all steps when scenario fails |

`--playwright-screenshots-dir` — Set directory for screenshots (default: ./screenshots)

### Playwright

Documentation for Playwright available [here](https://playwright.dev/python/docs/intro)
