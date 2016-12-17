from configurationData import TOKEN # Unique identifier
telegramURL = "https://api.telegram.org/"
baseURL     = telegramURL + "bot{}/".format(TOKEN)
baseFileURL = telegramURL + "file/bot{}/".format(TOKEN)

class TelegramUtil:

    def __init__(self):
        self.offset  = None
        self.getMsg  = baseURL + "getUpdates"
        self.sendMsg = baseURL + "sendMessage"
        self.getFile = baseURL + "getFile"

    def __makeRequest(self, url):
        # returns the response of a given url
        from requests import get
        response = get(url)
        content  = response.content.decode("utf-8")
        return content

    def __getJsonFromUrl(self, url):
        # given some url, return json response
        from json import loads
        return loads(self.__makeRequest(url))

    def __reOffset(self, updates):
        if len(updates) == 0:
            return
        li = []
        for update in updates:
            li.append(int(update["update_id"]))
        self.offset = max(li) + 1

    def getFilePath(self, fileId):
        url  = self.getFile + "?file_id={}".format(fileId)
        json = self.__getJsonFromUrl(url)['result']
        fpath = json['file_path']
        return baseFileURL + fpath
            
    def getUpdates(self):
        # Returns a json with the last messages the bot has received
        # If an offset is provided, we won't ask telegram for any previous messages 
        # we use longpolling to keep the connection open N seconds
        url = self.getMsg + "?timeout=100"
        if self.offset:
            url += "&offset={}".format(self.offset)
        updates = self.__getJsonFromUrl(url)
        result  = updates["result"]
        self.__reOffset(result)
        return result

    def sendMessage(self, text, chat):
        # Send a message given some id
        from urllib import parse
        text =  parse.quote_plus(text)
        url = self.sendMsg + "?text={}&chat_id={}".format(text, chat)
        self.__makeRequest(url)
        

