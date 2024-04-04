import csv
import random

# question type
UNKNOWN = -1
RAIN = 0
SNOW = 1
TEMP_COMP = 2
WEATHER_DATA = 3
WAKE_UP = 4

# TempComp
NA = 0
YES = 1

TOTAL_SAMPLE_SIZE = 80
SAMPLE_PER_QUESTION_TYPE = (int)(80 / 5)

# define fields
fields = ["sentence", "time", "location", "question_type", "temp_comp_flag"]

locations = [
    "N/A",
    "Boston",
    "New York",
    "London",
    "Paris",
    "Los Angeles",
    "Chicago",
    "Miami",
    "Tokyo",
    "Sydney",
    "Berlin",
    "Toronto",
    "Hong Kong",
    "Dubai",
    "Moscow",
    "Rome",
    "Madrid",
    "Seoul"
]

times = ["N/A", "now", "tomorrow", "next hour", "next week", "April 1st"]

def append_sentences(
    sentences: list, sentence_set: list, location, time, question_type, temp_comp_flag
):
    if location == "N/A" and time == "N/A":
        sentence = random.choice(sentence_set)
        sentence = sentence.format("", "")
    elif location == "N/A":
        sentence = random.choice(sentence_set)
        sentence = sentence.format("", time)
    elif location == "N/A":
        sentence = random.choice(sentence_set)
        sentence = sentence.format("in "+location, "")
    else:
        sentence = random.choice(sentence_set)
        sentence = sentence.format("in "+location, time)
    sentences.append(
        {
            "sentence": sentence,
            "time": time,
            "location": location,
            "question_type": question_type,
            "temp_comp_flag": temp_comp_flag,
        }
    )

# generate UNKWON sentence type
random_sentences = [
    "how are you",
    "what time is it",
    "do you prefer mac or linux",
    "it is cold outside",
    "it is raining",
    "it's so hot right now",
    "do you like the weather today"
]

# generate RAIN sentence type
general_rain_sentences = [
    "is it gonna rain {} {}",
    "will it rain {} {}",
    "is rain expected {} {}",
    "Might it rain {} {}"
]

# generate SNOW sentence type
general_snow_sentences = [
    "is it going to snow {} {}",
    "will it snow {} {}",
    "is snow expected {} {}",
    "Might it snow {} {}",
    "Do you think it will snow {} {}"
]

# generate TEMP_COMP sentence type
general_tempcomp_sentences = [
    "is it colder {} {}",
    "is it hotter {} {}",
    "will it be warmer {} {}",
    "will it be cooler {} {}",
    "how's the weather {} {} compared to right now"
]

# generate WEATHER_DATA type
general_weather_sentences = [
    "how is the weather {} {}",
    "tell me about the weather {} {}",
    "What's the weather like {} {}",
    "How's the climate {} {}",
    "Can you give me the weather conditions {} {}",
]

def generate_unknown_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = "N/A"
        time = "N/A"
        append_sentences(sentences, random_sentences, location, time, UNKNOWN, NA)

def generate_rain_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = random.choice(locations)
        time = random.choice(times)
        append_sentences(sentences, general_rain_sentences, location, time, RAIN, NA)

def generate_snow_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = random.choice(locations)
        time = random.choice(times)
        append_sentences(sentences, general_snow_sentences, location, time, SNOW, NA)

def generate_temp_comp_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = random.choice(locations)
        time = random.choice(times)
        append_sentences(sentences, general_tempcomp_sentences, location, time, TEMP_COMP, YES)

def generate_weather_data_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = random.choice(locations)
        time = random.choice(times)
        append_sentences(sentences, general_weather_sentences, location, time, WEATHER_DATA, NA)
        

# generate WAKE_UP type     
wake_up_sentences = [
    "Hey Simpson",
    "Hi Simpson"
]

def main():
    sentence_ls = []
    generate_unknown_sample(sentence_ls)
    generate_rain_sample(sentence_ls)
    generate_snow_sample(sentence_ls)
    generate_temp_comp_sample(sentence_ls)
    generate_weather_data_sample(sentence_ls)
    random.shuffle(sentence_ls)
    with open("training_dataset_updated_4.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sentence_ls)

main()