# AwesomeRasam

A BeautifulSoup4 wrapper for lazy people. Allows you to extract and clean HTML/XML into neat formats with very few lines of elegant code.

## Installation
```
pip3 install awesome-rasam
```

## Initializing

### From a URL
AwesomeRasam can use requests and BeautifulSoup4 under the hood to download html from an URL and create a soup object with it
```
from awesome_rasam import AwesomeRasam

rasam = AwesomeRasam("https://1upkd.com")
# or pass in any additional arguments you would pass to requests.get()
rasam = AwesomeRasam("https://1upkd.com",headers={"User-Agent":"Bot"})

print(rasam.get("title",">text"))
```

### From Text
Initialize the soup under-the-hood with HTML/XML formatted text. This is useful when you get HTML through a request session or through a headless browser.
```
from awesome_rasam import AwesomeRasam

html = "<html><head><title>Page Title</title></head><body>Hello</body></html>"
rasam = AwesomeRasam(html, features="html5lib")
```

### From a BeautifulSoup4 object
```
from awesome_rasam import AwesomeRasam
from bs4 import BeautifulSoup

html = "<html><head><title>Page Title</title></head><body>Hello</body></html>"
soup = BeautifulSoup(html, features="html5lib")
rasam = AwesomeRasam(soup)
```

## Scraping data
- All scraping is done by providing CSS selectors to pick elements, and the attributes to pick from those elements.
- In addition to the attributes present on element tag, special attributes `>text`, `>inner_markup`, `>outer_markup`, and `>rasam`
- `get()` and `get_all()` methods are provided to select first matching and all matching elements respectively
- If the element is not found, or the attributed is not present, an Exception is raised. This can be prevented by passing `flag=False`, and optional fallback value can be specified by passing `fallback="N/A"`
- A `pipe` argument can be passed containing a function or a list of functions to be executed on the result before returning
```
import json
from awesome_rasam import AwesomeRasam

rasam = AwesomeRasam("https://1upkd.com/host-website-on-laptop/")
blog = {
    "page_title": rasam.get("title", ">text"),
    "heading": rasam.get("h1", ">text"),
    "author": rasam.get(".title p>b", ">text"),
    "date": rasam.get(".title p>span", ">text", 
        pipe = lambda x: x.replace("\n","").strip()),
    "links": rasam.get_all("a","href"),
    "linked_emails": list(set(rasam.get_all(
        "a[href^='mailto:']", "href", 
        pipe = lambda x: x.split("mailto:")[1]))),
    "linked_emails_are_gmail": rasam.get_all(
        "a[href^='mailto:']", "href", 
        pipe = [
          lambda x: x.split("mailto:")[1],
          lambda x: x.endswith("@gmail.com")
        ]),
    "json_ld_metadata": rasam.get(
        "script[type='application/ld+json']", ">inner_markup",
        pipe=json.loads)        
}

print(json.dumps(blog, indent=2))
```

### Ultimate flex
```
import json
import random

from awesome_rasam import AwesomeRasam

def parse_blog(rasam):
    return {
        "page_title": rasam.get("title", ">text"),
        "heading": rasam.get("h1", ">text"),
        "author": rasam.get(".title p>b", ">text"),
        "date": rasam.get(".title p>span", ">text", 
            pipe = lambda x: x.replace("\n","").strip()),
        "links": rasam.get_all("a","href"),
        "linked_emails": list(set(rasam.get_all(
            "a[href^='mailto:']", "href", 
            pipe = lambda x: x.split("mailto:")[1]))),
        "linked_emails_are_gmail": rasam.get_all(
            "a[href^='mailto:']", "href", 
            pipe = [
              lambda x: x.split("mailto:")[1],
              lambda x: x.endswith("@gmail.com")
            ]),
        "json_ld_metadata": rasam.get(
            "script[type='application/ld+json']", ">inner_markup",
            pipe=json.loads)        
    }



rasam = AwesomeRasam("https://1upkd.com")
data = {
    "page_title": rasam.get("title", ">text"),
    "blogs": rasam.get_all("#blogs ~ a", "href", pipe=[
      lambda url: AwesomeRasam(
          "https://1upkd.com/"+url, 
          delay=random.randint(1,5)),
      parse_blog
    ])        
}

print(json.dumps(data, indent=2))
```
Note: The `delay` argument can be passed while initializing with URL, to delay the request by that many seconds. It can also be a function which returns the number of seconds.


