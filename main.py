from gpiozero import PWMLED
from time import sleep
import requests
import xmltodict
import re
from constants import colors, dot_colors

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

    color = "#FFFFFF"

    for i in range(len(dot_colors) - 1):
        opacity = (current_value - dot_colors[i]["tail"]) / (
            dot_colors[i + 1]["tail"] - dot_colors[i]["tail"]
        )
        if opacity >= 0 and opacity <= 1:
            color = colors[i + 1]["color2"]

    return hex_to_rgb(color)


def hex_to_pwm(hex):
    return hex / 255


def get_current_value(seconds, current_time):
    for second in seconds:
        if second["@t"] == current_time:
            return float(second["#text"])


def hex_to_rgb(hx, hsl=False):
    if re.compile(r"#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$").match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(
                int(hx[i] * 2, 16) / div if div else int(hx[i] * 2, 16)
                for i in (1, 2, 3)
            )
        else:
            return tuple(
                int(hx[i : i + 2], 16) / div if div else int(hx[i : i + 2], 16)
                for i in (1, 3, 5)
            )
    else:
        raise ValueError(f'"{hx}" is not a valid HEX code.')


main()
