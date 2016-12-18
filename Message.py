# The only reason for this class to exists is Order and Organisation

class Message:
# Variables that we are going to parse from json:
# chatId              - Id of the chat the message came from
# username            - user who sent the message
# isCommand           - t/f
# isRegisteredCommand - t/f
# isGroup             - t/f
# isFile              - t/f
# fileId              - file id
# text                - actual content of the message (minus /command)
# command             - command given in /command (or "")
# ignore              - t/f (whether this message should be ignored)

    def __init__(self, jsonDict):
        # Global variables
        registeredCommands = ["poder", "habilidad", "store"]
        # ignore keys:
        ik1 = "new_chat_participant"
        ik2 = "left_chat_participant"
        msg = "message"
        self.json = jsonDict
        keys      = jsonDict.keys()
        if msg not in keys:
            msg = "edited_message"
        try:
            message = jsonDict[msg]
        except:
            print("   >>>>> ")
            print(jsonDict)
            raise Exception("Not a message or an edited message?")
        msgKeys  = message.keys()
        if ik1 in msgKeys or ik2 in msgKeys:
            self.ignore = True
            return
        else:
            self.ignore = False
        fromData = message['from']
        chatData = message['chat']
        # Populate general fields
        self.username = fromData['username']
        self.chatId   = chatData['id']
        if "text"  in msgKeys:
            self.text = message["text"]
        elif "caption" in msgKeys:
            self.text = message["caption"]
        if chatData['type'] == 'group':
            self.isGroup = True
        else:
            self.isGroup = False
        if self.text[0] == '/':
            self.isCommand = True
        else:
            self.isCommand           = False
            self.command             = ""
            self.isRegisteredCommand = False
        if self.isCommand:
            allText      = self.text.split(' ', 1)
            self.command = allText[0][1:]
            # Absorb the @ in case is it a directed command
            if '@' in self.command:
                self.command = self.command.split('@')[0]
            self.text    = allText[-1]
            if self.command in registeredCommands:
                self.isRegisteredCommand = True
            else:
                self.isRegisteredCommand = False
        if "photo" in msgKeys:
            self.isFile = True
            photoData   = message["photo"][-1]
            self.fileId = photoData["file_id"]
        else:
            self.isFile = False


        




