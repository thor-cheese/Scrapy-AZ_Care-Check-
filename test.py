def create_json():
    with open('/Users/adevoid/documents/scrapeAZCareCheckProject/residential_facilities.json', 'w') as outfile:
        pass
    # csvOpen = open('/Users/adevoid/documents/scrapeAZCareCheckProject/residential_facilities.csv', 'w')
    # csv.writer(csvOpen)
    # print('NEW')
def append_new_obj(file_name, data):
    # Open file in append mode
    with open(file_name) as read_json:
        data = json.load(read_json)
    result = data

    with open(file_name, 'a+', newline='') as write_obj:
        data = json.load(f)
