from handle_request import WeatherAssistant, TempComp

def main():
    assistant = WeatherAssistant()
    # assistant.weather_data_handler()
    
    assistant.temp_comp = TempComp.COLD
    assistant.time = 'tomorrow'
    # assistant.temp_cmp_handler()
    assistant.is_snow_handler()
    assistant.is_rain_handler()
    
main()