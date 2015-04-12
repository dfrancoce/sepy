import datetime, os, errno

class Util:

    def createDirectory(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def getUrls(self):
        now = datetime.datetime.now()
        start = 2006
        end = now.year + 1

        url = "http://www.se-radio.net/"
        urls = []

        for i in range(start, end): # years
            for j in range(1,13): # months
                urls.append(url + str(i) + "/" + str(j))
                self.createDirectory("data/" + str(i) + "/" + str(j))

        return urls
