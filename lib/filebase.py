from firebase import firebase
import json
import os
from lib.utils import remove_common_elements, generate_unique_code, Counter

class FileBaseApplication(object):
    def __init__(self, firebase_URL, opfile='data.json', changes_file='changes.json', changes_firebase_file='changes_firebase.json'):
        self._data = {}
        self._firebase = firebase.FirebaseApplication(firebase_URL, None)
        self._opfile = opfile
        self._chfile = changes_file
        self._changes = {}
        self._changes_firebase_file = changes_firebase_file
        self._changes_firebase = {}
        self._data = self._get_data()
        
        if os.path.isfile(self._chfile):
            with open(self._chfile) as datafile:
                self._changes = json.load(datafile)
                
        if os.path.isfile(self._changes_firebase_file):
            with open(self._changes_firebase_file) as changes_file:
                self._changes_firebase = json.load(changes_file)
    
    def _get_data(self):

        if os.path.isfile(self._opfile):
            print( "file found")
            with open(self._opfile) as data_file:
                data = json.load(data_file)
        else:
            print("file not found")
            # self._pull_data()
            return self._firebase.get('/', None)    
        return data
    
    def _pull_data(self):
        # data = self._firebase.get('/', None)
        data = self._data
        if "edits" in self._data.keys():
            # Get the highest key you have
            edit_keys = map(int, self._data["edits"].keys())
            max_edit_key = max(edit_keys)
            firebase_edits = self._firebase.get('/edits', None)
            firebase_edit_keys = map(int, firebase_edits.keys())
            max_firebase_edit_key = max(firebase_edit_keys)
            if max_edit_key <  max_firebase_edit_key:
                edits_to_apply = {key: firebase_edits[key] for key in firebase_edits.keys() if int(key) > max_edit_key}
                self._apply_edits(edits_to_apply)
            
        with open(self._opfile, 'w') as outfile:
            json.dump(data, outfile)
        
    def _apply_edits(self, edits):
        insert_set = set()
        delete_set = set()
        for key, edit in edits.items():
            if "ADD" in edit.keys():
                for inserted_item in edit["ADD"]:
                    insert_set.add(inserted_item)
            if "DELETE" in edit.keys():
                for deleted_item in edit["DELETE"]:
                    delete_set.add(deleted_item)
            self.put('/edits', key, edit, log=False)
        
        # Delete common elements from both sets
        
        common_set = insert_set.intersection(delete_set)
        insert_set = insert_set - common_set
        delete_set = delete_set - common_set
        
        # Apply the remaining changes.
        for inserted_item in insert_set:
            print("inserting ", inserted_item)
            url, name = self._get_name_from_url(inserted_item)
            data = self._firebase.get(url, name)
            self.put(url, name, data, log=False)
        for deleted_item in delete_set:
            print("deleting ", deleted_item)
            url, name = self._get_name_from_url(deleted_item)
            self.delete(url, name, log=False)
            
        
        
        
                
    def _get_data_from_url(self, url):
        url_components = filter(lambda x: x != '', url.split("/"))
                
        result = self._data
        for comp in url_components:
            if comp not in result.keys():
                result[comp] = {}
            result = result[comp]
        return result
    
    def _add_to_changes(self, change, url, changes=None):
        if change not in  ["ADD", "EDIT", "DELETE"]:
            print("Invalid Change String")
            raise ValueError("Invalid Change String... Use one of ADD, EDIT or DELETE")
        if change in changes.keys():
            if url not in changes[change]:
                changes[change].append(url)
        else:
            changes[change] = [url]
            
    def _add_url_and_name(self, url, name):
        url_components = list(filter(lambda x: x != '', url.split("/")))
        result_url = ""
        if url_components:
            result_url +=  "/" + "/".join(url_components)
        result_url += "/" + name
        return result_url
    
    def _get_name_from_url(self, url):
        url_components = list(filter(lambda x: x != '', url.split("/")))
        name = url_components[-1]
        url_res = "/" + "/".join(url_components[:-1])
        return (url_res, name)
        
    def get(self, url, name=None, log=True):
        result = self._get_data_from_url(url)
        if name is not None:
            if name not in result.keys():
                result[name] = None
            result = result[name]
         
        return result
    
    def put(self, url, name, data, log=True):
        result = self._get_data_from_url(url)
        result[name] = data
        full_url = self._add_url_and_name(url, name)
        if log:
            self._add_to_changes("ADD", full_url, changes=self._changes)
        
    def patch(self, url, newdata, log=True):
        result = self._get_data_from_url(url)
        
        for key in newdata.keys():
            result[key] = newdata[key]
        
        if log:
            self._add_to_changes("EDIT", url, changes=self._changes)
    def delete(self, url, name, log=True):
        
        result = self._get_data_from_url(url)
        
        del result[name]
        full_url = self._add_url_and_name(url, name)
        if log:
            self._add_to_changes("DELETE", full_url, changes=self._changes)

    def save(self):
        with open(self._opfile, 'w') as outfile:
            json.dump(self._data, outfile)
        with open(self._chfile, 'w') as outfile:
            json.dump(self._changes, outfile)
        
    
    def _minimize_changes(self):
        add_list, edit_list, delete_list = [], [], []
        
        if "ADD" in self._changes.keys():
            add_list = self._changes["ADD"]
        if "EDIT" in self._changes.keys():
            edit_list = self._changes["EDIT"]
        if "DELETE" in self._changes.keys():
            delete_list = self._changes["DELETE"]
        add_list, edit_list, delete_list = remove_common_elements(add_list, edit_list,  delete_list)
        add_list, delete_list, _ = remove_common_elements(add_list, delete_list)
        edit_list, _, _ = remove_common_elements(edit_list, add_list)
        edit_list, _, _ = remove_common_elements(edit_list, delete_list)
        
        
        self._changes["ADD"] = add_list
        self._changes["EDIT"] = edit_list
        self._changes["DELETE"] = delete_list
        
    
    def _process_changes(self):
        try:
            
            print("applying changes....")
            inserts = self._changes["ADD"] if "ADD" in self._changes.keys() else []
            inserts += self._changes["EDIT"] if "EDIT" in  self._changes.keys() else []
            deletes = self._changes["DELETE"] if "DELETE" in self._changes.keys() else []
            

            for r in inserts:
                data = self.get(r, None)
                url, name = self._get_name_from_url(r)
                self._firebase.put(url, name, data)
                self._add_to_changes("ADD", r, self._changes_firebase)

            for d in deletes:
                url_res, name_res = self._get_name_from_url(d)
                self._firebase.delete(url_res, name_res)
                self._add_to_changes("DELETE", d, self._changes_firebase)
                
            if self._changes_firebase:
                editnumber = self._firebase.get('/counter', 'edits') + 1
                self._firebase.put('/counter', 'edits', editnumber)
                self._firebase.put('/edits', editnumber, self._changes_firebase)
                self.put('/edits',str(editnumber), self._changes_firebase)
        except Exception as e:
            with open(self._changes_firebase_file, 'w') as outfile:
                json.dump(self._changes_firebase, outfile)
            raise e

    
    def sync(self):
        self._minimize_changes()
        self._process_changes()
        if os.path.isfile(self._chfile):
            os.remove(self._chfile)
        if os.path.isfile(self._changes_firebase_file):
            os.remove(self._changes_firebase_file)
        self._pull_data()
    
    def get_unique_counter_code(self):
        code = generate_unique_code(4)
        while code in self._data["counter"].keys():
            code = generate_unique_code(4)
        return code
        
        
        
         
        
        
        
    
