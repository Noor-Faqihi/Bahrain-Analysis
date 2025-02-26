from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd 

def collect_flight_data(day,flight_direction):
    '''
    this function collects the data from bahrain airport and return it as a table
    arg:
    day(str): it will be today(td) or tomorrow (tm).
    flight_direction (str): it will return arrival or departure
    returns:
    oandas dataframe that has 7b columns
    '''
    url=f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    time_lst=[]
    destination=[]
    airways_lst=[]
    gate_lst=[]
    status_lst=[]
    flight_lst=[]
    
    # if flight_direction == 'arrivals':
    #     flights = soup.find_all("div", {"class": "flight-table-list row dvArrivalList"})
    # elif flight_direction == 'departures':
    #       flights = soup.find_all("div", {"class": "flight-table-list row dvDeparturesList"})

    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"}) #ArrivalList
    
    #flights = soup.find_all("div", {"class": "flight-table-list row dvArrivalList"})
    for flight in flights:
    # print(i)
        try:
            airways_lst.append(flight.find('img')['alt'])
        except:
            airways_lst.append(pd.NA)
        flight_lst.append(flight.find('div',class_="col col-flight-no").text.strip())
        status_lst.append(flight.find('div',class_="col col-flight-status").text.strip())
        gate_lst.append(flight.find('div',class_="col col-gate").text.strip())
        # airways_lst.append(flight.find('img'))
        time_lst.append(flight.find('div',class_="col col-flight-time").text.strip())
        destination.append(flight.find('div',class_="col col-flight-origin").text.strip())
        flights_data={'origin': destination,
                      'flight Nm':flight_lst,
                      'airline':airways_lst,
                      'gate':gate_lst,
                      'status':status_lst,
                      'time':time_lst}
        df=pd.DataFrame(flights_data)
        TODAY_DATE= datetime.date.today()
        TOMORROW_DATE= TODAY_DATE +datetime.timedelta(days=1)
        if day=='TD':
            date=TODAY_DATE
        elif day=='TM':
            date=TOMORROW_DATE
        df['date']=date
        df['direction']=flight_direction
    return df

def collect_arr_dep():
    directions = ['arrivals','departures']
    days = ['TD', 'TM'] 
    total_data = [] 
    for direction in directions:
        for day in days:
            total_data.append(collect_flight_data(day,direction)) 
            time.sleep(10) 
    df = pd.concat(total_data) 
    return df 

def save_df(df):
    today = datetime.date.today()
    path = f'BH_Airport_{today}.csv'.replace('-','_')
    df.to_csv(path) 