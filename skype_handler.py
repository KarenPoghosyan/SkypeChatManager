from skpy import Skype, SkypeChats
from getpass import getpass


class SkypeHandler:

    def connect(self, user, password):
        self.sk = Skype(user, password)  # connect to Skype

    def get_contacts(self):
        return self.sk.contacts

    def get_chats(self):
        while True:
            lst = self.sk.chats.recent()
            for k,v in lst.items():
                if hasattr(v, 'topic'):
                    print(str(k)+ str(v.topic))
            else:
                break
        return SkypeChats(self.sk)

    def get_chat(self, id_str):
        return self.sk.chats[id_str]






        # ch = sk.chats.create(["joe.4", "daisy.5"]) # new group conversation
        # ch = sk.contacts["joe.4"].chat # 1-to-1 conversation

        # ch.sendMsg("fffff") # plain-text message
        # ch.sendFile(open("song.mp3", "rb"), "song.mp3") # file upload
        # ch.sendContact(sk.contacts["daisy.5"]) # contact sharing

        # ch.getMsgs() # retrieve recent messages