import datetime
from pyscript import fetch, document


url = 'YOUR OWN API KEY I AM NOT DOING THIS MISTAKE AGAIN'
data = await fetch(url, method="GET").json()


def get_days():
    days = []
    i = 0

    while True:
        try:
            str_day = data['timelines']['daily'][i]['time']
            parsed_day = datetime.datetime.strptime(str_day, "%Y-%m-%dT%H:%M:%SZ")
            day = parsed_day.strftime("%d-%m")
            days.append(day)
            i += 1
        except Exception:
            if not days:
                print("Maximum API Keys reached, try again in a couple minutes or an hour")
            
            break
    return days


def temp_days(days):
    temperatures = [] # TempAVG, TempMIN, TempMAX

    for i in range(len(days)):
        tempAVG = data['timelines']['daily'][i]['values']['temperatureAvg']
        tempMin = data['timelines']['daily'][i]['values']['temperatureMin']
        tempMax = data['timelines']['daily'][i]['values']['temperatureMax']
        temperatures.append((tempAVG, tempMin, tempMax))
    return temperatures


def buildInfo(days, temps):

    if not days:
        outputText1 = "Keine Wetterinformationen wurden gefunden.\nDer API Key ist wahrscheinlich gerade im Cooldown."
    
    else:
        i = 0
        outputText1 = f""
        outputText2 = f""
        dayStats = zip(days, temps)

        for stat in dayStats:
            if i % 2 == 0:
                outputText1 += f"{stat[0]}:\nDurchschnittliche Temperatur:\t{stat[1][0]}°C\nMinimale Temperatur:\t\t{stat[1][1]}°C\nMaximale Temperatur:\t\t{stat[1][2]}°C\n\n"
            else:
                outputText2 += f"{stat[0]}:\nDurchschnittliche Temperatur:\t{stat[1][0]}°C\nMinimale Temperatur:\t\t{stat[1][1]}°C\nMaximale Temperatur:\t\t{stat[1][2]}°C\n\n"
            i += 1
    
    try:
        outputDiv = document.querySelector('#info')
        outputDiv2 = document.querySelector('#info2')
        outputDiv.innerText = outputText1
        outputDiv2.innerText = outputText2
    except:
        pass

days = get_days()
print(days)
temps = temp_days(days)

buildInfo(days, temps)