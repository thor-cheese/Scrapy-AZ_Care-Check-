import scrapy
import csv
from csv import writer
import json
from scrapy.loader import ItemLoader
from scrapeAZCareCheckProject.items import ScrapeazcarecheckprojectItem, Scrapeazcarecheckproject_enforcement_Item, Count_Facilities_Item


class Count_Facilities(scrapy.Spider):
    name = 'Count_Facilities'
    start_urls = ['https://hsapps.azdhs.gov/ls/sod/SearchProv.aspx?type=AL']
    download_delay = 0
    count = 0

    def parse(self, response):

        print('parse')
        yield scrapy.FormRequest(
            'https://hsapps.azdhs.gov/ls/sod/SearchProv.aspx?type=AL',
            formdata={

                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),

                'ctl00$ContentPlaceHolder1$DropDownListPvType': 'AL',
                'ctl00$ContentPlaceHolder1$btnSubmit1': 'Start Search'
            },
            callback=self.pagnation
        )


    def pagnation(self, response):

        
        print('pagnation')
        hf1 = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField1"]/@value').extract_first()
        hf2 = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField2"]/@value').extract_first()
        current_page = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_ddPage"]/option[@selected]/@value').extract_first()
        total_pages = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblTotalPages"]//text()').extract_first()


        next_page = int(current_page) +1


        facilities = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_DgFacils"]//tr')
        for facility in facilities[1:]:
            # print(facility.xpath("td[1]//a/@href").re(r"(?<=\,')(.*?)(?=\')"))
            self.count += 1

            idx = self.count

            seachResults = {}


            select = facility.xpath("td[1]//a/@href").re(r"\,'(.*?)\'")

            name = facility.xpath('td[2]//text()').extract_first()

            address = facility.xpath('td[3]//text()').extract_first()

            city_state = facility.xpath('td[4]//text()').extract_first()
            type = facility.xpath('td[5]//text()').extract_first()

            loader = ItemLoader(item=Count_Facilities_Item(), selector=facility)
            loader.add_xpath('name', 'td[2]//text()')
            loader.add_xpath('address', 'td[3]//text()')
            loader.add_xpath('city_state', 'td[4]//text()')
            loader.add_xpath('facility_type', 'td[5]//text()')
            yield loader.load_item()


        if int(current_page) <= int(total_pages):
            yield scrapy.FormRequest(
                'https://hsapps.azdhs.gov/ls/sod/Provider.aspx?type=AL',
                formdata={
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddPage',
                    # '__EVENTARGUMENT': '',
                    '__VIEWSTATEENCRYPTED':'',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    'ctl00$ContentPlaceHolder1$ddPage':str(next_page),
                    'ctl00$ContentPlaceHolder1$HiddenField1': hf1,
                    'ctl00$ContentPlaceHolder1$HiddenField2': hf2

                },
                callback=self.pagnation
            )
