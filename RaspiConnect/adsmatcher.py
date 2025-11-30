from random import random


class AdMatcher:
    def __init__(self):
        self.DEFAULT_VIDEO = "b0099_01.mp4"

        self.rules = [
            #KIDS
            {"min_age": 0, "max_age": 17, "gender": None, "video": "b0017_01.mp4"},
            {"min_age": 0, "max_age": 17, "gender": "Male", "video": "m0017_02.mp4"},

        ]

        def select_ad(self, gender, age):
            if age is None: age = 25
            if gender is None: gender = "Male"

            try:
                age = int(age)
            except ValueError:
                age = 25

            print("Admatcher: Selecting ad for Age:", age, "Gender:", gender)

            matched_video = []

            for rule in self.rules:
                #check age
                if rule["min_age"] <= age <= rule["max_age"]:

                    #check gender
                    if rule["gender"] is None or rule["gender"].lower() == gender.lower():
                        matched_video.append(rule["video"])

            if matched_video:
                selected = random.choice(matched_video)
                print("Admatcher: Matched video:", selected, "from ", len(matched_video), "candidates.")
                return selected
            else:
                print("Admatcher: No match found, using default video.")
                return self.DEFAULT_VIDEO