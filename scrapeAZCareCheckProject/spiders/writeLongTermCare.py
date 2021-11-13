import scrapy
import csv
from csv import writer
import json
from scrapy.loader import ItemLoader
from scrapeAZCareCheckProject.items import ScrapeazcarecheckprojectItem, Scrapeazcarecheckproject_enforcement_Item


class SpidyQuotesViewStateSpider1(scrapy.Spider):
    name = 'azCareCheckCrawler-longTermCare'
    start_urls = ['https://hsapps.azdhs.gov/ls/sod/Provider.aspx?type=LTC']
    download_delay = 2
    count = 0

    def parse(self, response):
        print('parse')
        yield scrapy.FormRequest(
            'https://hsapps.azdhs.gov/ls/sod/Provider.aspx?type=LTC',
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
        print(hf1)
        print(hf2)
        print(current_page)
        next_page = int(current_page) + 1
        print(next_page)


        facilities = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_DgFacils"]//tr')
        for facility in facilities[1:]:
            # print(facility.xpath("td[1]//a/@href").re(r"(?<=\,')(.*?)(?=\')"))
            self.count += 1

            idx = self.count

            seachResults = {}


            select = facility.xpath("td[1]//a/@href").re(r"\,'(.*?)\'")
            print(select)
            name = facility.xpath('td[2]//text()').extract_first()
            print(name)
            address = facility.xpath('td[3]//text()').extract_first()

            city_state = facility.xpath('td[4]//text()').extract_first()
            type = facility.xpath('td[5]//text()').extract_first()

            loader = ItemLoader(item=ScrapeazcarecheckprojectItem(), selector=facility)
            loader.add_xpath('name', 'td[2]//text()')
            loader.add_xpath('address', 'td[3]//text()')
            loader.add_xpath('city_state', 'td[4]//text()')
            loader.add_xpath('facility_type', 'td[5]//text()')
            # yield loader.load_item()

            # name = Field()
            # address = Field(),
            # city_state = Field(),
            # facility_type = Field()
            # survey_date = Field()
            # survey_description = Field()

            seachResults[self.count] = {
                'name': name,
                'address': address,
                'city_state':city_state,
                'type':type
            }

            # append_index_json(seachResults,idx)


            yield scrapy.FormRequest(
                'https://hsapps.azdhs.gov/ls/sod/Provider.aspx?type=AL',
                formdata={
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$DgFacils',
                    '__EVENTARGUMENT': select,
                    '__VIEWSTATEENCRYPTED':'',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    'ctl00$ContentPlaceHolder1$ddPage':current_page,
                    'ctl00$ContentPlaceHolder1$HiddenField1': hf1,
                    'ctl00$ContentPlaceHolder1$HiddenField2': hf2

                },
                callback=self.parse_residence,

                meta={'name':name, 'index':idx,'current_page':current_page, 'address':address, 'city_state':city_state,'type':type}
            )


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

    def parse_residence(self, response):
        # facility_row = response.meta.get('facility')
        current_page = response.meta.get('current_page')
        address = response.meta.get('address')
        city_state = response.meta.get('city_state')
        type = response.meta.get('type')
        print(current_page)
        name = response.meta.get('name')
        index = response.meta.get('index')

        #parse inspections / surveys table before request
        surveys = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvInspections"]//tr')
        for survey in surveys[1:]:
            # print(facility.xpath("td[1]//a/@href").re(r"(?<=\,')(.*?)(?=\')"))
            print(name)
            # date = survey.xpath('td[2]//text()').extract_first()
            # facility_row.append(date)

            # print(date)


            # print('survey date: '+ date)
            select = survey.xpath("td[1]//a/@href").re(r"\,'(.*?)\'")

            hf3 = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField3"]/@value').extract_first()

            #hf2 is also the facility ID
            hf2 = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField2"]/@value').extract_first()

            #request inspections / surveys
            yield scrapy.FormRequest(
                'https://hsapps.azdhs.gov/ls/sod/Facility.aspx?FacId='+hf2,
                formdata={
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvInspections',
                    '__EVENTARGUMENT': select,
                    '__VIEWSTATEENCRYPTED':'',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    'ctl00$ContentPlaceHolder1$ddPage':current_page,
                    # 'ctl00$ContentPlaceHolder1$HiddenField1': hf1,
                    'ctl00$ContentPlaceHolder1$HiddenField2': hf2,
                    'ctl00$ContentPlaceHolder1$HiddenField3': hf3

                },
                callback=self.parse_survey,

                meta={'name':name,'index':index, 'address':address,'city_state':city_state,'type':type}
            )



        enforcements = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvEnfDates"]//tr')
        for enforcement in enforcements[1:]:

            select_enforcement = enforcement.xpath("td[1]//a/@href").re(r"\,'(.*?)\'")

        #request enforcement actions
            yield scrapy.FormRequest(
                'https://hsapps.azdhs.gov/ls/sod/Facility.aspx?FacId='+hf2,
                formdata={
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvEnfDates',
                    '__EVENTARGUMENT': select_enforcement,
                    '__VIEWSTATEENCRYPTED':'',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    'ctl00$ContentPlaceHolder1$ddPage':current_page,
                    # 'ctl00$ContentPlaceHolder1$HiddenField1': hf1,
                    'ctl00$ContentPlaceHolder1$HiddenField2': hf2,
                    'ctl00$ContentPlaceHolder1$HiddenField3': hf3

                },
                callback=self.parse_enforcement,

                meta={'name':name,'index':index, 'address':address,'city_state':city_state,'type':type}
            )





    #parse inspections / surveys
    def parse_survey(self, response):
        # facility_row = response.meta.get('facility')
        name = response.meta.get('name')
        index = response.meta.get('index')
        # name_item = response.meta.get('name_item')
        address = response.meta.get('address')


        city_state = response.meta.get('city_state')
        type = response.meta.get('type')

        print('parse inspections')



        date = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblSurveyDate"]//text()').extract_first()



        description = response.css('.lefttext.bottompad10::text').extract()



        survey_item = ScrapeazcarecheckprojectItem()


        survey_item['name'] = name
        survey_item['address'] = address
        survey_item['facility_type'] = type
        survey_item['city_state'] = city_state

        survey_item['survey_date'] = date
        survey_item['survey_description'] = description[0].strip()

        yield survey_item






    #parse inspections / surveys
    def parse_enforcement(self, response):
        # facility_row = response.meta.get('facility')
        name = response.meta.get('name')
        index = response.meta.get('index')
        # name_item = response.meta.get('name_item')
        address = response.meta.get('address')

        city_state = response.meta.get('city_state')
        type = response.meta.get('type')

        print('parse enforcements')


        enforcement_date = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblFileClosedDate"]//text()').extract_first()

        license = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblProvLicense2"]//text()').extract_first()

        address_from_page = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblEnfAdr"]//text()').extract_first()

        name_from_page = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblProvName2"]//text()').extract_first()

        civil_penalty = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblCivilPenalty"]//text()').extract_first()



        enforcement_description = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblDecision"]//text()').extract_first()

        enforcement_item = Scrapeazcarecheckproject_enforcement_Item()

        enforcement_item['name'] = name
        enforcement_item['facility_type'] = type
        enforcement_item['city_state'] = city_state
        enforcement_item['address'] = address
        enforcement_item['name_from_page'] = name_from_page
        enforcement_item['license'] = license
        enforcement_item['address_from_page'] = address_from_page

        enforcement_item['enforcement_date'] =enforcement_date
        enforcement_item['civil_penalty'] = civil_penalty
        enforcement_item['enforcement_description'] = enforcement_description

        yield enforcement_item
