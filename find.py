import requests
from bs4 import BeautifulSoup

def find_36hr():
    url="https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-02897EC8-E5F8-4C66-B4E7-F1B907E9328E&format=JSON"
    try:
        find=requests.get(url).json()
        location=find['records']['location']
        datass=[]
        for i in range(len(location)):
            locationName=location[i]['locationName']
            weatherElement=location[i]['weatherElement']
            datas=[]
            for i in range(len(weatherElement)):
                elementName=weatherElement[i]['elementName']
                time=weatherElement[i]['time']
                data=[]
                for t in time:
                    startTime=t['startTime']
                    endTime=t['endTime']
                    parameter=t['parameter']['parameterName']
                    data.append([locationName,elementName,startTime,endTime,parameter])
                datas.extend(data)
            datass.extend(datas)
        return datass
    except Exception as e:
        print(e)
        return None
    
def find_news(tag,number=1):
    url="https://tw.news.yahoo.com/tag/"+tag
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,"lxml")
    mbs=soup.find_all('h3',class_="Mb(5px)")[:number]
    data=[]
    for mb in mbs:
        href=mb.find('a').get('href')
        newurl=url+href
        resp=requests.get(newurl)
        soup=BeautifulSoup(resp.text,"lxml")
        title=soup.find('div',class_='caas-title-wrapper').text
        tv=soup.find('img',class_='caas-img').text
        source=soup.find('div',class_='caas-attr-item-author').text
        time=soup.find('div',class_='caas-attr-time-style').text
        body_html=soup.find('div',class_='caas-body').find_all('p')
        data.append([title,tv,source,time,body_html])
    return data

def shift_time(time):
    m=time.split(' ')[0].split('-')[1]
    d=time.split(' ')[0].split('-')[2]
    h=time.split(' ')[1].split(':')[0]
    if h[0]=='0':
        h=h[1]
    if int(h)<=12:
        simple_time=m+'/'+d+' 上午'+h+':00'
    else:
        simple_time=m+'/'+d+' 下午'+str(int(h)-12)+':00'
    return simple_time

def find_city_data(numstr):
    url='https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWA-02897EC8-E5F8-4C66-B4E7-F1B907E9328E&locationId=F-D0047-'+numstr
    find=requests.get(url).json()
    locationsName=find['records']['locations'][0]['locationsName'] #縣市
    locations=find['records']['locations'][0]['location']
    datass=[]
    for location in locations:
        datas=[]
        locationName=location['locationName'] #鄉鎮市區
        weatherElements=location['weatherElement']
        for weatherElement in weatherElements:
            description=weatherElement["description"]
            times=weatherElement['time']
            data=[description]
            for time in times:
                if 'startTime' in time:
                    startTime=shift_time(time['startTime'])
                    endTime=shift_time(time['endTime'])
                    elementValue=time['elementValue'][0]['value']
                    data.append([startTime,endTime,elementValue])
                elif 'dataTime' in time:
                    dataTime=shift_time(time['dataTime'])
                    elementValue=time['elementValue'][0]['value']
                    data.append([dataTime,elementValue])
            datas.append(data)
        datass.append([locationName,datas])
    return locationsName,datass

def get_json(weather,xAxis,yAxis):
    json_data={'title':weather,"x":xAxis,"y":yAxis}
    return json_data