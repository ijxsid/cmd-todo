from firebase import firebase
import json

class FileBaseApplication(object):
    def __init__(self, firebase_URL, opfile):
        self._data = {}
        self._firebase = firebase.FirebaseApplication(firebase_URL, None)
        self._opfile = opfile
        self._data = self._firebase.get('/', None)
        
        with open(self._opfile, 'w') as outfile:
            json.dump(self._data, outfile)
            
    
    def get(self, url, name):
        
        url_components = filter(lambda x: x != '', url.split("/"))
        
        url_components.append(name)
        
        result = self._data
        for comp in url_components:
            result = result[comp]
        
        return result
        
        
         
        
        
        
    
