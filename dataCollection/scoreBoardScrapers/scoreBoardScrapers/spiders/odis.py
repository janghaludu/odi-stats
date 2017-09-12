# -*- coding: utf-8 -*-
import scrapy


class OdisSpider(scrapy.Spider):
    name = 'odis'
    allowed_domains = ['howstat.com']
    baseUrl = 'http://www.howstat.com/cricket/Statistics/Matches/MatchScorecard_ODI.asp?MatchCode='
    matchIds = range(45, 4000)
    

    def parse(self, response):
        links = [self.baseUrl + matchId for matchId in self.matchIds]
		for link in links:
			yield scrapy.Request(link, callback=self.getMatchData)


	def getMatchData(self, response):
		# Get Match Title. For Ex -  1972 England v Australia - 3rd Match - Birmingham
		titleTable = response.xpath('//body/table/tr/td[@width = "100%"]').xpath('table')
		title = titleTable[0].xpath('tr/td[@class="ScoreCardBanner2"]/text()')[0].extract().strip()
		# Get Match Meta Data -  MatchDate, Venue, MatchConditions, Toss, Result, ManOfMatch
		metaData = {}
		metaDataRows = response.xpath('//table[@cellpadding=1]')[1].xpath('tr')
		for row in metaDataRows:
			 metaData[row.xpath('td/text()')[0].extract().strip()] = \
			 		  row.xpath('td/text()')[1].extract().strip()
		# Get Scoreboard
		scoreBoard = {}
		scoreBoardRows = response.xpath('//table[@cellpadding=1]')[2].xpath('tr')	 		  
		inningsStartRows = filter(lambda row: len(row.xpath('td')) == 7, scoreBoardRows)
		batsmanRows = filter(lambda row: len(row.xpath('td')) == 8, scoreBoardRows)
		extrasRows = filter(lambda row: 'Extras' in row.xpath('td/text()')[0].extract(), scoreBoardRows)
		totalRows = filter(lambda row: 'Total' in row.xpath('td/text()')[0].extract(), scoreBoardRows)
		fallOfWicketsRows = filter(lambda row: 'll of Wi' in row.xpath('td/text()')[0].extract(), scoreBoardRows)
		bowlerRows = filter(lambda row: row.xpath('td/table/tr/td/a'), scoreBoardRows)


		#batsmanColumns = sorted(zip(list(range(1,3))*11, list(range(1,12))*2), key=lambda x: x[0])
		batsmanColumns = [ (innings, batsman) for innings in range(1,3) for batsman in range(1,12)]






