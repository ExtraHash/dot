from gpiozero import PWMLED
from time import sleep
import requests
import xmltodict
import re
import math
from constants import colors, color_weights

blue_led = PWMLED(23)
red_led = PWMLED(24)
green_led = PWMLED(25)


def main():
    while True:
        set_led(get_dot_color())
        sleep(5)


def set_led(rgb):
    red_led.value = hex_to_pwm(rgb[0])
    green_led.value = hex_to_pwm(rgb[1])
    blue_led.value = hex_to_pwm(rgb[2])


def get_dot_color():
    res = xmltodict.parse(requests.get("http://gcpdot.com/gcpindex.php").text)

    current_time = res["gcpstats"]["serverTime"]
    data = res["gcpstats"]["ss"]["s"]

    current_value = get_current_value(data, current_time)

    out_color = colors[0]

    for i in range(len(color_weights) - 1):
        opacity = (current_value - color_weights[i]) / (
            color_weights[i + 1] - color_weights[i]
        )
        if opacity >= 0 and opacity <= 1:
            out_color = colors[i + 1]
            blend_color = colors[i + 2]
            inv_opacity = 1 - opacity

            r = math.floor(blend_color[0] * opacity + inv_opacity * out_color[0])
            g = math.floor(blend_color[1] * opacity + inv_opacity * out_color[1])
            b = math.floor(blend_color[2] * opacity + inv_opacity * out_color[2])

            out_color = (r, g, b)
            print(out_color)

    return out_color


def hex_to_pwm(hex):
    return hex / 255


def get_current_value(seconds, current_time):
    for second in seconds:
        if second["@t"] == current_time:
            return float(second["#text"])


main()
