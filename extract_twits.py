import json
import os
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


############## create url and path to save ######################

base_url = 'https://api.stocktwits.com/api/2/streams/symbol/'
todo_list =  os.path.join('C:\\Users', 'divernoi', 'Dropbox','ticker_list_todo.txt')
access_token_list = ['1f884b1423fc42db61e12420c637798a619e19f8',
                     'c0f3bf6f489610fdedcd780b2772f7e14c3553f2',
                     '6e8e76779c49dfbfb3026dd924321f3fa8b151a7',
                     'fafc63990c17bbd74d0578d28031723754154e48',
                     'ff553307d39b44bfde2ced9f8391effae61a79f2',
                     'dd1941bed2f0db234223b9f8182fc7b4251a4f28',
                     '0f2f4d0ae5a6ed783f647fe259cd797caa001657',
                     '693226ee6815b6231bb6f285c692d2b891ff4b27',
                     '88dc7edc7ec59156e1fd8f2a25f6bb3fa7c17a62']

ticker_list = []
f = open(os.path.join('C:\\Users','divernoi','Dropbox','ticker_list_todo.txt'),"r", encoding="utf8")
lines = f.readlines()
f.close()

for line in lines:
    ticker_list.append(line.rstrip())

ticker_error = []


def alternate():                        # tiny func to alternate between access token
    while True:
        yield access_token_list[0]
        yield access_token_list[1]
        yield access_token_list[2]
        yield access_token_list[3]
        yield access_token_list[4]
        yield access_token_list[5]  
        yield access_token_list[6]
        yield access_token_list[7]
        yield access_token_list[8]


alternator = alternate()

################ loop to request json for every ticker ########### UUUUUUUUUUUUU

start_twit_id = '132884946'     # local start id for first ticker in loop

for ticker in ticker_list:
    no_more = False
    directory_path = os.path.join('C:\\Users', 'MarcAurele Divernois', 'Dropbox\JSON', ticker)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    while no_more == False:
        json_url = base_url + ticker + '.json?access_token='+ alternator.__next__() +'&max=' + str(start_twit_id)         #url
        path_to_save = os.path.join('C:\\Users', 'MarcAurele Divernois', 'Dropbox', 'JSON', ticker,
                                    ticker + '_' + str(start_twit_id) + '.txt')  # directory path for laptop epfl
        # retry connection 3 times if fail
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=4.6)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        get_json = session.get(json_url)
        try:
            load_json = json.loads(get_json.text)                           #json object
        except:
            print("I retry because of decode error")
            time.sleep(18.1)
            get_json = session.get(json_url)
            load_json = json.loads(get_json.text)
        error_code = load_json['response']['status']
        if error_code == 200:                                         #check that request is success
            no_more = load_json['messages'] == []
            if no_more == False:
                start_twit_id = load_json['cursor']['max']
                twit_start_time = load_json['messages'][0]['created_at']
                twit_end_time = load_json['messages'][-1]['created_at']
                print('ticker: ' + ticker + ', id: ' + str(
                    start_twit_id) + ', time: from ' + twit_start_time + ' to ' + twit_end_time)
                with open(path_to_save, "w") as write_file:
                    json.dump(load_json, write_file)                        #save to file
        elif error_code == 429:
            print('Sorry I had to wait...!')
            time.sleep(3601)
        else:
            print('error code: ' + str(error_code) + ' for ticker ' + ticker)
            no_more = True
            ticker_error.append(ticker)
        time.sleep(1)                                                  #wait 9sec
    f = open(todo_list, "r")                                         #remove ticker from todo list
    lines = f.readlines()
    f.close()
    f = open(todo_list, "w")
    for line in lines:
        if line != ticker + "\n":
            f.write(line)
    f.close()
    start_twit_id = '132884946'         # general starting id - twit created_at : 2018-08-07T12:04:53Z


# write ticker errors to txt file

f = open(os.path.join('C:\\Users', 'MarcAurele Divernois', 'Dropbox','ticker_error.txt'), 'a')
for ticker in ticker_error:
    f.write(ticker + ' ')
f.close()


#200 - Success
#400 - Bad Request
#401 - Unauthorized
#403 - Forbidden
#404 - Not Found
#422 - Unprocessable Entity
#429 - Too Many Requests
#500 - Internal Server Error
#503 - Service Unavailable
#504 - Gateway Timeout






####################### open json file #########################
# with open('JSON\AA.txt', encoding="utf8") as json_file:
#    data34 = json.load(json_file)

#for file in os.listdir('JSON')


############ post request to get access token ###############

# r = requests.post("https://api.stocktwits.com/api/2/oauth/token", data={'client_id': '4da4e30027544fb4', 'client_secret': 'f69871404b8052b697eb59b3a6138530dcdcbaaf','code' : '034eb5cc9296965ac3019ade77af3b5efab64d61' ,'grant_type': 'authorization_code','redirect_uri':'https://stocktwits.com/'})


