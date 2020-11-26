from gpiozero import PWMLED
from time import sleep
import requests
import xmltodict

blue_led = PWMLED(23)
red_led = PWMLED(24)
green_led = PWMLED(25)

def set_color(red, green, blue):
    red_led.value = convert(red)
    green_led.value = convert(green)
    blue_led.value = convert(blue)

def convert(hex):
    return hex/255

def get_color():
    res = requests.get("http://gcpdot.com/gcpindex.php")
    dot_data = xmltodict.parse(res.text)

    server_time = dot_data["gcpstats"]["serverTime"]
    seconds = dot_data["gcpstats"]["ss"]["s"]

    current_second = get_current_second(seconds, server_time)
    print(current_second)
            
def get_current_second(seconds, current_time):
    for second in seconds:
        if second["@t"] == current_time:
            return second
    


get_color()