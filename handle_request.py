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
        return url

    def weather_data_handler(self):
        api_type = self.acquire_api_type()
        url = self.acquire_url(api_type)

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)
        else:
            raise Exception("unable to fetch weather data")
