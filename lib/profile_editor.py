from clint.textui import colored
from utils import EMAIL_REGEX
class ProfileEditor(object):
    def __init__(self, profile):
        self._profile = profile['info'] if 'info' in profile.keys() else {}


    def editflow(self):
        profile = self._profile
        info = {}
        name = profile['name'] if 'name' in profile.keys() else ''
        try:
            new_name = (raw_input("What's your name, Salior?("+name+")").strip() or name)
            if new_name == '':
                raise ValueError
        except ValueError:
            raise ValueError(colored.red("Your name can't be an Empty String."))
        info['name'] =  new_name
        email = profile['email'] if 'email' in profile.keys() else ''
        try:
            new_email = (raw_input("Do you Email, ?("+email+")").strip() or email)
            email_re_match = EMAIL_REGEX.match(new_email)
            print email_re_match
            if new_email == '' or email_re_match is None:
                raise ValueError
        except ValueError:
            raise ValueError(colored.red("Your email might not be an valid one."))
        info['email'] = new_email

        return info
