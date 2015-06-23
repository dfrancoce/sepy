import datetime, os, errno

class Util:
    urls = []
    url = "http://www.se-radio.net/"

    def createDirectory(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def getUrls(self, year, month):
        if (not year is None):
            if (not month is None):
                self.appendMonthToUrl(int(year), int(month))
            else:
                self.iterateMonths(int(year))
        else:
            now = datetime.datetime.now()
            start = 2006
            end = now.year + 1
            self.iterateYears(start, end)

        return self.urls

    def iterateYears(self, start, end):
        for year in range(start, end):
            self.iterateMonths(year)

    def iterateMonths(self, year):
        for month in range(1,13): # months
            self.appendMonthToUrl(year, month)

    def appendMonthToUrl(self, year, month):
        self.urls.append(self.url + str(year) + "/" + str(month))
        self.createDirectory("data/" + str(year) + "/" + str(month))
