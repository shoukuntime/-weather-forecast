from flask import Flask, render_template
from find import find_36hr,find_news,shift_time,find_city_data,get_json
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/36hr")
def for36hr():
    data=find_36hr()
    cities=[]
    for i in data:
        if i[0] not in cities:
            cities.append(i[0])
    return render_template("36hr.html",data=data,cities=cities)

@app.route("/36hr/city=<city>")
def for36hrcity(city):
    city=city
    datas=find_36hr()
    data=[]
    for d in datas:
        if d[0]==city:
            data.append(d)
    times=[t[2] for t in datas[:3]]
    newdata=[]
    for t in times:
        new=[shift_time(t)]
        for d in data:
            if d[2]==t:
                new.extend([d[4]])
        new[3]=new[3]+'~'+new[5]
        newdata.append(new[:5])
    return render_template("36hrcity.html",data=newdata,times=times,city=city)

@app.route("/news")
def news():
    tags=['氣象','颱風','空氣','氣溫','降雨']
    return render_template("news.html",tags=tags)

@app.route("/newstag/tag=<tag>")
def newstag(tag):
    tag=tag
    return render_template("newstag.html",find_news=find_news,tag=tag)

@app.route("/2daydetail")
def for2daydetail():
    city_id={
        "001":"宜蘭縣",
        "005":"桃園市",
        "009":"新竹縣",
        "013":"苗栗縣",
        "017":"彰化縣",
        "021":"南投縣",
        "025":"雲林縣",
        "029":"嘉義縣",
        "033":"屏東縣",
        "037":"臺東縣",
        "041":"花蓮縣",
        "045":"澎湖縣",
        "049":"基隆市",
        "053":"新竹市",
        "057":"嘉義市",
        "061":"臺北市",
        "065":"高雄市",
        "069":"新北市",
        "073":"臺中市",
        "077":"臺南市",
        "081":"連江縣",
        "085":"金門縣",
        "089":"台灣",
    }
    
    return render_template("2daydetail.html",city_id=city_id)

@app.route("/2daydetail/city=<city>&id=<id>")
def for2daydetailcity(city,id):
    city=city
    id=id
    datas=find_city_data(id)
    return render_template("2daydetailcity.html",city=city,datas=datas[1],id=id)

@app.route("/2daydetail/city=<city>&id=<id>/town=<town>")
def for2daydetailtown(city,id,town):
    city=city
    id=id
    town=town
    datas=find_city_data(id)
    for i in range(len(datas[1])):
        if datas[1][i][0]==town:
            data=datas[1][i][1]
            break
    return render_template("2daydetailtown.html",city=city,datas=data,id=id,town=town)

@app.route("/2daydetail/city=<city>&id=<id>/town=<town>/weather=<weather>")
def for2daydetailweather(city,id,town,weather):
    city=city
    id=id
    town=town
    weather=weather
    datas=find_city_data(id)
    for i in range(len(datas[1])):
        if datas[1][i][0]==town:
            data=datas[1][i][1]
            for d in data:
                if d[0]==weather:
                    detail=d[1:]
                    xAxis=[]
                    yAxis=[]
                    
                    for s in d[1:]:
                        if isinstance(s[-1], (int, float)):
                            if len(s)==3:
                                xAxis.extend([s[0]+' ~ '+s[1]])
                                yAxis.extend([int(s[2])])
                            else:
                                xAxis.extend([s[0]])
                                yAxis.extend([int(s[1])])
                    
                        else:
                            if len(s)==3:
                                xAxis.extend([s[0]+' ~ '+s[1]])
                                yAxis.extend([s[2]])
                            else:
                                xAxis.extend([s[0]])
                                yAxis.extend([s[1]])
                        
    return render_template("2daydetailweather.html",city=city,data=detail,id=id,town=town,weather=weather,xAxis=xAxis,yAxis=yAxis)


@app.route("/2daydetail_chart/city=<city>&id=<id>/town=<town>/weather=<weather>")
def for2daydetailweather_chart(city,id,town,weather):
    city=city
    id=id
    town=town
    weather=weather
    datas=find_city_data(id)
    for i in range(len(datas[1])):
        if datas[1][i][0]==town:
            data=datas[1][i][1]
            for d in data:
                if d[0]==weather:
                    detail=d[1:]
                    try:
                        xAxis=[]
                        yAxis=[]
                        for s in detail:
                            if len(s)==3:
                                xAxis.extend([s[0]+' ~ '+s[1]])
                                yAxis.extend([int(s[2])])
                            else:
                                xAxis.extend([s[0]])
                                yAxis.extend([int(s[1])])
                        json_data=get_json(weather,xAxis,yAxis)
                    except:
                        json_data=None
    return json.dumps(json_data,ensure_ascii=False)


app.run(host="0.0.0.0")