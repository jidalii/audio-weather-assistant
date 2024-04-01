import csv
import random

# question type
UNKNOWN = -1
RAIN = 0
SNOW = 1
TEMP_COMP = 2
WEATHER_DATA = 3

# TempComp
NA = -1
COLD = 0
HOT = 1

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
]
times = ["N/A", "now", "tomorrow", "next hour", "next week", "April 1st"]


def append_sentences(
    sentences: list, sentence, location, time, question_type, temp_comp_flag
):
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

# generate RAIN sentence type

# generate SNOW sentence type

# generate TEMP_COMP sentence type

# generate WEATHER_DATA type
general_weather_sentences = [
    "how is the weather {} {}",
    "tell me about the weather {} {}",
    "What's the weather like {} {}",
    "How's the climate {} {}",
    "Can you give me the weather conditions {} {}",
]


def generate_weather_data_sample(sentences: list):
    for i in range(SAMPLE_PER_QUESTION_TYPE):
        location = random.choice(locations)
        time = random.choice(times)
        if location == "N/A" and time == "N/A":
            sentence = random.choice(general_weather_sentences)
            sentence = sentence.format("", "")
            append_sentences(sentences, sentence, location, time, WEATHER_DATA, NA)
        elif location == "N/A":
            sentence = random.choice(general_weather_sentences)
            sentence = sentence.format("", time)
            append_sentences(sentences, sentence, location, time, WEATHER_DATA, NA)
        elif location == "N/A":
            sentence = random.choice(general_weather_sentences)
            sentence = sentence.format("in "+location, "")
            append_sentences(sentences, sentence, location, time, WEATHER_DATA, NA)
        else:
            sentence = random.choice(general_weather_sentences)
            sentence = sentence.format("in "+location, time)
            append_sentences(sentences, sentence, location, time, WEATHER_DATA, NA)


def main():
    sentence_ls = []
    generate_weather_data_sample(sentence_ls)
    with open("training_dataset.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sentence_ls)


main()
