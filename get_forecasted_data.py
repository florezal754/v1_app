import requests 
import pandas as pd 

def get_values(df):
    #make API call
    TOKEN = open('Token.txt', 'r').read()
    headers = {'content-Type': 'application/json', 'Authorization': 'Token token={}'.format(TOKEN)}
    #Miurl = "https://api.esios.ree.es/indicators/3"
    #print(Miurl)
    
    market_info = [3,4,9,14,15,16,18,21,22,10064,10073,10086,10095,10167,10258,28,29,30,31,25,26,10104,10113,10122,10131,10186,10196,10141]
    print("Total of indicators: ", len(market_info))
    urls = []
    data = []
    
    for ids in market_info:
        Miurl = "https://api.esios.ree.es/indicators/"+str(ids)
        urls.append(Miurl)
        #print(Miurl)
        response = requests.get(Miurl, headers=headers).json()
        indicators = response['indicator']['short_name']
        print(indicators)
        #time.sleep(1)
        #print(response)
        
        for value in response['indicator']['values']:
            PBF_value = value['value']
            PBF_datetime = value['datetime']
            PBF_datetime_utc = value['datetime_utc']
            PBF_tz_time = value['tz_time']
            PBF_datetime = PBF_datetime.replace('Z', "")
            PBF_shortname = response['indicator']['short_name']
            #PBF_hour = PBF_datetime.replace('2022-05-14T', "")
            #PBF_hour = PBF_hour.replace(':00:00', "")

            #saving to pandas dataframe
            df = df.append({'PBF_shortname':PBF_shortname,
                            'PBF_value':PBF_value, 
                            'PBF_datetime':PBF_datetime,
                            'PBF_datetime_utc':PBF_datetime_utc,
                            'PBF_tz_time':PBF_tz_time}, ignore_index=True)

        
    return df 

#2. set datetime index to operate with time series data 
def set_datetime_index(df):
    df.PBF_datetime = pd.to_datetime(df.PBF_datetime, utc=True)
    df = df.set_index(df.PBF_datetime)
    df = df.drop('PBF_datetime', axis=1)

    return df 

def sort_pivot(df):
    #short df per date
    #df = df.sort_values(by=['PBF_datetime'])
    df = pd.pivot_table(df, values='PBF_value', index=['PBF_datetime'],columns=['PBF_shortname'])
    
    return df





