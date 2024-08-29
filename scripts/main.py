import datetime, matplotlib.pyplot as plt, numpy as np, mplcursors as mpl
from pyscript import fetch, display

url = 'YOUR OWN API KEY I AM NOT DOING THIS MISTAKE AGAIN'
json = await fetch(url, method="GET").json()
print(url, json)

def get_days(data=None):
    if data is None:
        data = json

    days = []
    i = 0

    while True:
        try:
            str_day = data['timelines']['daily'][i]['time']
            parsed_day = datetime.datetime.strptime(str_day, "%Y-%m-%dT%H:%M:%SZ")
            day = parsed_day.strftime("%d-%m")
            days.append(day)
            i += 1
        except Exception as e:
            print(e)
            break
    return days

def temp_days(days, data=None):
    if data is None:
        data = json

    temperatures = [] # TempAVG, TempMIN, TempMAX

    for i in range(len(days)):
        tempAVG = json['timelines']['daily'][i]['values']['temperatureAvg']
        tempMin = json['timelines']['daily'][i]['values']['temperatureMin']
        tempMax = json['timelines']['daily'][i]['values']['temperatureMax']
        temperatures.append((tempAVG, tempMin, tempMax))
    return temperatures


def parse_temps(temps):
    avgtemp = []
    mintemp = []
    maxtemp = []

    for i in range(len(temps)):
        avgtemp.append(temps[i][0])
        mintemp.append(temps[i][1])
        maxtemp.append(temps[i][2])
    return avgtemp, mintemp, maxtemp

def draw_graph(days, temps):
    '''
    Essentially when I subtract a number (in this case 0.25) from an np.array() it subtracts that amount from every single int() value inside of the array
    which is very neat as you dont have to do some weird loop shit
    '''

    x_labels = days
    x_axis = np.arange(len(days))
    tempAVG, tempMIN, tempMAX = parse_temps(temps)

    tempAVG = np.array(tempAVG)
    tempMIN = np.array(tempMIN)
    tempMAX = np.array(tempMAX)

    fig, axs = plt.subplots(1, 2, figsize=(12, 3), sharex=True, sharey=True)
    fig.tight_layout() 
    fig.suptitle('Durchschnittliche, minimale und maximale Temperatur')

    bar_width = 0.2

    x_pos1 = x_axis - bar_width
    x_pos2 = x_axis
    x_pos3 = x_axis + bar_width

    axs[0].bar(x_pos1, tempAVG, width=bar_width, label='Average Temp')
    axs[0].bar(x_pos2, tempMIN, width=bar_width, label='Minimum Temp')
    axs[0].bar(x_pos3, tempMAX, width=bar_width, label='Maximum Temp')
    axs[1].plot(x_labels, tempAVG, label='Average Temp')
    axs[1].plot(x_labels, tempMIN, label='Minimum Temp')
    axs[1].plot(x_labels, tempMAX, label='Maximum Temp')

    plt.xticks(x_axis, x_labels)
    plt.legend()
    mpl.cursor(hover=True)

    # plt.show()
    display(fig, target="mpl")


days = get_days()
temps = temp_days(days)
draw_graph(days, temps)