import scrapy

#Need to take out " for names, messing up conversion to JSON

class ProfileSpider(scrapy.Spider):
    name = "profiles"
    def start_requests(self):
        
        self.counter = 0
        urls = []
        results_per_page = 50
        total_results = 60000
        
        for increment in range(0, int(total_results/results_per_page)):
            temp_url = "https://usatt.simplycompete.com/userAccount/s?format=&max=" + str(results_per_page) + "&offset=" + str(increment*results_per_page)
            #print(increment)
            urls.append(temp_url)
    
        #urls = ['https://usatt.simplycompete.com/userAccount/s?format=&max=50&offset=0']
        
        #urls = ['https://usatt.simplycompete.com/userAccount/s?format=&max=225&offset=1']
        for link in urls:
            yield scrapy.Request(url = link, callback = self.parse)
            
                
    def parse(self, response):
        #page = response.url.split("/")[-2]
        
        self.counter = self.counter + 1
            #filename = 'profiles/profiles-%s.html' % page
        profile_ids = getProfileIds(self, response)
        profile_names = getProfileNames(self, response)
        profile_ratings = getProfileRatings(self, response)
        profile_locations = getProfileLocations(self, response)
        print("****************************************")
        print("")
        print("Processing link number: " + str(self.counter))
        print("")
        print("ID LENGTH: " + str(len(profile_ids)))
        print("NAME LENGTH: " + str(len(profile_names)))
        print("RATING LENGTH: " + str(len(profile_ratings)))
        print("LOCATION LENGTH: " + str(len(profile_locations)))
        print("****************************************")
        writeToCSV(profile_ids, profile_names, profile_ratings, profile_locations)

def getProfileNames(self, response):
    return response.xpath('//div[@class = "img-text"]//a/text()').extract()

def getProfileLocations(self, response):
    locations = response.xpath('//td[@class = "list-column mobile-hide"]/text()').extract()
    new_locations = []
    locations_no_lines = []
    for location in locations:
        if '\n' in location:
            location_no_line = location.replace('\n','')
        locations_no_lines.append(location_no_line)
    for item in locations_no_lines:
        if ',' in item:
            new_location = item.replace(',                  ', ': ')
        else:
            new_location = item
        new_locations.append(new_location.strip())
    return new_locations

def getProfileRatings(self, response):
    ratings = response.xpath('//tr[@class="list-item"]//td[@class="list-column text-center"]/text()').extract()
    ratingList = []
    for count, item in enumerate(ratings):
        if(count % 2 == 0):
            ratingList.append(item)
    return ratingList

def getProfileIds(self, response):
    ids = response.xpath('//tr[@class="list-item"]//td[@class="list-column text-center"]/text()').extract()
    idList = []
    for count, item in enumerate(ids):
        if(count % 2 == 1):
            idList.append(item)
    return idList

def writeToCSV(IDLIST, NAMELIST, RATINGLIST, LOCATIONLIST):
    file = open('profiles/profile_data_4_16_2018.csv','a')
    
    for i in range(len(IDLIST)):
        tempString = str(IDLIST[i]) + "," + NAMELIST[i] + "," + str(RATINGLIST[i]) + "," + LOCATIONLIST[i] + "\n"
        file.write(tempString)
    file.close()
#self.log('saved file %s' % file)






