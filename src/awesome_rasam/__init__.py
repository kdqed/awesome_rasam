# __init__.py

__version__ = "0.0.6"

import time
import traceback

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

default_features = "html5lib"

class AwesomeRasam:
    
    def __init__(self, initializer, *args, **kwargs):
        if isinstance(initializer, str):
            if (initializer.startswith("http://") 
                    or initializer.startswith("https://")):
                if 'delay' in kwargs:
                    if callable(kwargs['delay']):
                        time.sleep(kwargs['delay']())
                    else:
                        time.sleep(kwargs['delay'])
                    del kwargs['delay']       
                r = requests.get(initializer, **kwargs)
                self._soup = BeautifulSoup(r.text, features=default_features)
            else:
                self._soup = BeautifulSoup(initializer, *args, **kwargs)
        elif (isinstance(initializer, BeautifulSoup) 
              or isinstance(initializer, Tag)):
            self._soup = initializer
        else:
            error_text = "Intializer must be url string, html/xml string, BeautifulSoup or bs4.Element.Tag, but got {} object"
            error_text = error_text.format(type(initializer))
            raise UnsupportedInitializer(error_text)    
                    
    
    @staticmethod
    def _get_attribute(el, selector, attribute, pipe=[], attribute_flag=True, fallback=None):
        
        if attribute==">text":
            extract = el.text
        elif attribute==">inner_markup":
            extract = el.decode_contents()
        elif attribute==">outer_markup":
            extract = str(el)
        elif attribute==">rasam":
            extract = AwesomeRasam(el)    
        else:
            extract = el.get(attribute)
            if extract is None:
                if attribute_flag:
                    raise AttributeIsNone("selector={} & attribute={}".format(selector, attribute))
                else:
                    return fallback
        
        if callable(pipe):
            pipe = [pipe]
        
        for f in pipe:
            extract = f(extract)    
                    
        return extract                                                    
    
    def get(self, selector, attribute, pipe=[], flag=True, fallback=None):
        if selector==">self":
            el = self._soup
        else:
            el = self._soup.select_one(selector)
            if el:
                pass
            elif flag:
                raise ElementNotFound(selector)
            else:
                return fallback
                
        return AwesomeRasam._get_attribute(el, selector, attribute, pipe, flag, fallback)         
    
    def get_all(self, selector, attribute, pipe=[], flag=True, attribute_flag=True, fallback=None):
        el_list = self._soup.select(selector)
        if el_list:
            pass
        elif flag:
            raise NoElementsFound(selector)
        else:
            return []
        
        results = []
        for el in el_list:
            results.append(AwesomeRasam._get_attribute(el, selector, attribute, pipe, attribute_flag, fallback))    
        
        return results                    

class UnsupportedInitializer(Exception):
    pass        

class ElementNotFound(Exception):
    pass

class NoElementsFound(Exception):
    pass

class AttributeIsNone(Exception):
    pass
    

if __name__=="__main__":
    pass
    '''url = "https://wios.xyz"
    print(AwesomeRasam(url, headers={"User-Agent": "Bot"})._soup.title)
    r = requests.get(url)
    print(AwesomeRasam(r.text, features="html5lib")._soup.title)
    print(AwesomeRasam(BeautifulSoup(r.text, features="html5lib"))._soup.title)
    AwesomeRasam(6, headers={"User-Agent": "Bot"})
    
    rasam = AwesomeRasam("https://wios.xyz", delay=1)
    print(rasam.get("header",">text"))
    print(rasam.get("header",">inner_markup"))
    print(rasam.get("header",">outer_markup"))
    print(rasam.get("header",">rasam").get("a",">rasam").get(">self",">outer_markup"))
    print(rasam.get("a[href^='https://']","href",pipe = [
        lambda x: x.split("https://")[1],
        lambda x: "http://" + x
    ]))
    rasam = AwesomeRasam("https://1upkd.com", delay=1)
    print(rasam.get_all("a[href^='https://']","href",pipe=[
        lambda x: AwesomeRasam(x, delay=1).get("title",">text",flag=False)
    ],attribute_flag=False, fallback="lol"))'''
            
