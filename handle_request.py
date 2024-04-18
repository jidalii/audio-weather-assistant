import os
from dotenv import load_dotenv
import requests
from dataclasses import dataclass
from enum import Enum
from typing import Union

load_dotenv()


# question type
class QuestionType(Enum):
    UNKNOWN = -1
    RAIN = 0
    SNOW = 1
    TEMP_COMP = 2
    WEATHER_DATA = 3
    WAKE_UP = 4


# TempComp
class TempComp(Enum):
    NA = 0
    COLD = 1
    HOT = 2


@dataclass
class WeatherAssistant:
    question_type: QuestionType = QuestionType.UNKNOWN
    temp_comp: TempComp = TempComp.NA
    location: str = "N/A"
    time: str = "N/A"
    sentence: str = ""
    is_awake: bool = False

    def request_handler(self) -> None:
        if self.question_type == QuestionType.WAKE_UP:
            self.wake_up()
        elif self.question_type == QuestionType.UNKNOWN:
            self.unknown_handler()
        elif self.question_type == QuestionType.WEATHER_DATA:
            self.weather_data_handler()

    def wake_up(self) -> None:
        if self.is_awake == True:
            print("I am here.")
        else:
            self.is_awake = True
            print("What can I do for you?")

    def unknown_handler(self) -> None:
        print(f"I don't understand {self.sentence}. Please try a different question.")

    def acquire_geolocation(self) -> Union[float, float] | Exception:
        url = "http://ip-api.com/json/?fields=lat,lon"
        response = requests.get(url)
        if response.status_code == 200:
            geolocation = response.json()
            return geolocation["lat"], geolocation["lon"]
        else:
            raise Exception("unable to fetch geolocation")

    def acquire_api_type(self) -> str:
        """_summary_:
        helper function

        Returns:
            str: api_type, `realtime` or `forecast`
        """
        if self.time == "N/A" or self.time == "today":
            api_type = "realtime"
        else:
            api_type = "forecast"
        return api_type

    def acquire_url(self, api_type: str) -> str:
        """_summary_
        helper function: return the url with correct params
        Args:
            api_type (str): `realtime` or `forecast`

        Returns:
            str: url for the weather api call
        """
        if self.location == "N/A":
            lat, lon = self.acquire_geolocation()
            url = "https://api.tomorrow.io/v4/weather/{}?location={},{}&units=metric&apikey={}".format(
                api_type,
                lat,
                lon,
                os.environ["TOMORROW_WEATHER_API_KEY"],
            )
        else:
            url = "https://api.tomorrow.io/v4/weather/{}?location={}&units=metric&apikey={}".format(
                api_type,
                self.location,
                os.environ["TOMORROW_WEATHER_API_KEY"],
            )
        if api_type == "forecast":
            url += "&timesteps=1d"
        return url

    def weather_data_handler(self):
        api_type = self.acquire_api_type()
        url = self.acquire_url(api_type)

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_values = weather_data["data"]["values"]
            # print(weather_values)
            print(f"Current tempareture: {weather_values['temperature']}")
            print(f"Weather condition: {weather_values['weatherCode']}")
            print(f"Chance of raining: {weather_values['rainIntensity']}")
            print(f"Chance of snowing: {weather_values['snowIntensity']}")
            print(f"Windspeed: {weather_values['windSpeed']}")

        else:
            raise Exception("unable to fetch weather data")

    def print_temp_comp_msg(self, data_cmp: dict, isHotter: bool):
        weather_str = f"From {data_cmp['min']} to {data_cmp['max']}"
        if self.temp_comp == TempComp.COLD:
            if isHotter:
                print(f"No, {self.time} not is colder. {weather_str}")
            else:
                print(f"Yes, {self.time} is colder. {weather_str}")
        elif self.temp_comp == TempComp.HOT:
            if isHotter:
                print(f"Yes, {self.time} is hotter. {weather_str}")
            else:
                print(f"No, {self.time} not is hotter. {weather_str}")
        else:
            print("error: invalid temp_comp_flag")

    def temp_cmp_handler(self):
        api_type = self.acquire_api_type()
        url = self.acquire_url(api_type)
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            # print(weather_data)
            weather_values = weather_data["timelines"]["daily"]
            data_today_raw = weather_values[0]["values"]
            data_today = {
                "avg": data_today_raw["temperatureAvg"],
                "min": data_today_raw["temperatureMax"],
                "max": data_today_raw["temperatureMin"],
            }
            if self.time == "tomorrow":
                data_cmp_raw = weather_values[1]["values"]
                data_cmp = {
                    "avg": data_cmp_raw["temperatureAvg"],
                    "min": data_cmp_raw["temperatureMax"],
                    "max": data_cmp_raw["temperatureMin"],
                }
            elif self.time == "next week":
                data_cmp_raw = weather_values[7]["values"]
                data_cmp = {
                    "avg": data_cmp_raw["temperatureAvg"],
                    "min": data_cmp_raw["temperatureMax"],
                    "max": data_cmp_raw["temperatureMin"],
                }
            print(data_today)
            print(data_cmp)

            if data_today["avg"] > data_cmp["avg"]:
                isHotter = True
            else:
                isHotter = False

            self.print_temp_comp_msg(data_cmp, isHotter)

    def is_snow_handler(self):
        api_type = self.acquire_api_type()
        url = self.acquire_url(api_type)
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_data = weather_data["timelines"]["daily"]
            if self.time == "tomorrow":
                data_cmp = weather_data[1]["values"]
            elif self.time == "next week":
                data_cmp = weather_data[7]["values"]
            snow = data_cmp["snowIntensityAvg"]
            if snow == 0:
                print(f"No snow {self.time}.")
            else:
                print(
                    f"There would be snow {self.time} with avg {snow} mm/hr"
                )
    
    def is_rain_handler(self):
        api_type = self.acquire_api_type()
        url = self.acquire_url(api_type)
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_data = weather_data["timelines"]["daily"]
            if self.time == "tomorrow":
                data_cmp = weather_data[1]["values"]
            elif self.time == "next week":
                data_cmp = weather_data[7]["values"]
            snow = data_cmp["rainIntensityAvg"]
            if snow == 0:
                print(f"No rain {self.time}.")
            else:
                print(
                    f"There would be rain {self.time} with avg {snow} mm/hr"
                )

