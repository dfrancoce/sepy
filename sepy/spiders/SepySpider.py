import scrapy, urllib

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from sepy.items import SepyItem
from sepy.util import Util

class SepySpider(BaseSpider):
    name = "sepy"
    allowed_domains = ["se-radio.net"]

    def __init__(self, year=None, month=None, *args, **kwargs):
        super(SepySpider, self).__init__(*args, **kwargs)
        util = Util()
        self.start_urls = util.getUrls(year, month)

    def encodeString(self, stringToEncode):
        return stringToEncode.encode('utf-8', 'replace')

    def parse(self, response):
        for x in response.xpath('//a[@class="more-link"]'):
            yield scrapy.Request(self.getExtractedURL(x), callback=self.parseDownloadURL)

    def getExtractedURL(self, x):
        extractedURL = x.xpath('@href').extract()
        return self.encodeString(extractedURL[0])

    def parseDownloadURL(self, response):
        downloadFolder = self.resolveDownloadFolder(response)

        item = SepyItem()
        item["url"] = self.getDownloadURL(response)
        item["name"] = downloadFolder + "/" + self.getDownloadName(response)
        item["info"] = self.getDownloadInfo(response)
        infoPath = downloadFolder + "/" + self.getDownloadName(response) + ".html"

        self.download(item["name"], item["url"], item["info"], infoPath)

    def resolveDownloadFolder(self, response):
        return "data/" + response.url.split("/")[3] + "/" + str(int(response.url.split("/")[4]))

    def getDownloadURL(self, response):
        extractedURL = response.xpath('//a[@title="Download"]').xpath('@href').extract()

        return self.encodeString(extractedURL[0])

    def getDownloadName(self, response):
        extractedName = response.xpath('//a[@title="Download"]').xpath('@download').extract()

        return self.encodeString(extractedName[0])

    def getDownloadInfo(self, response):
        extractedInfo = response.xpath('//div[@class="entry"]/p[1]').extract()

        return self.encodeString(extractedInfo[0])

    def download(self, name, url, info, infoPath):
        self.writeInfoFile(info, infoPath)

        self.log('Downloading %s' % url)
        urllib.urlretrieve (url, name)

    def writeInfoFile(self, info, infoPath):
        infoFile = open(infoPath, "w")
        infoFile.write(info)
        infoFile.close()
