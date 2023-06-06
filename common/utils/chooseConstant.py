


from datetime import datetime


LANGUAGE_CHOICES = [
    ('english', 'English'),
    ('spanish', 'Spanish'),
    ('chinese', 'Chinese'),
    ('hindi', 'Hindi'),
    ('vietnamese', 'Vietnamese'),
    ('korean', 'Korean'),
    ('french', 'French'),
    ('german', 'German'),
    ('arabic', 'Arabic'),
    ('russian', 'Russian'),
    ('japanese', 'Japanese'),
    ('portuguese', 'Portuguese'),
    ('italian', 'Italian'),
    ('polish', 'Polish'),
    ('ukrainian', 'Ukrainian'),
    ('tagalog', 'Tagalog'),
    ('persian', 'Persian'),
    ('gujarati', 'Gujarati'),
    ('bengali', 'Bengali'),
    ('hebrew', 'Hebrew'),
    ('punjabi', 'Punjabi'),
    ('tamil', 'Tamil'),
    ('marathi', 'Marathi'),
    ('turkish', 'Turkish'),
    ('thai', 'Thai'),
    ('nepali', 'Nepali'),
    ('swahili', 'Swahili'),
    ('amharic', 'Amharic'),
    ('greek', 'Greek'),
    ('dutch', 'Dutch'),
    ('czech', 'Czech'),
    ('swedish', 'Swedish'),
    ('danish', 'Danish'),
    ('norwegian', 'Norwegian'),
    ('finnish', 'Finnish'),
    ('hungarian', 'Hungarian'),
    ('romanian', 'Romanian'),
]

#ActiveDutyFlag
DUTY_FLAG_CHOICES =[('ActiveDuty','Active Duty'),('NonActive','Non Active'),]
#Discharge YEAR
DISCHARGE_YEAR_CHOICES = range(1900, datetime.now().year)
#Military BRANCH
BRANCH = [
    ('army', 'Army'),
    ('Navy', 'Navy'),
    ('marines', 'Marines'),
    ('coast-guard', 'Coast Guard'),
    ('air-force', 'Air Force'),
    ('others', 'Others'),
]
#Military RANK
RANK_CHOICES = [
    ('', 'Select Rank'),
    ('E-1 Seaman recruit', 'E-1 Seaman recruit'),
    ('E-2 Seaman apprentice', 'E-2 Seaman apprentice'),
    ('E-3 Seaman', 'E-3 Seaman'),
    ('E-4 Petty Officer 3rd class', 'E-4 Petty Officer 3rd class'),
    ('E-5 Petty Officer 2nd class', 'E-5 Petty Officer 2nd class'),
    ('E-6 Petty Officer 1st class', 'E-6 Petty Officer 1st class'),
    ('E-7 Chief Petty Officer', 'E-7 Chief Petty Officer'),
    ('E-8 Senior Chief Petty Officer', 'E-8 Senior Chief Petty Officer'),
    ('E-9 Master Chief Petty Officer', 'E-9 Master Chief Petty Officer'),
    ('E-9 Command Master Chief Petty Officer', 'E-9 Command Master Chief Petty Officer'),
    ('E-9 Master Chief Petty Officer of the Navy', 'E-9 Master Chief Petty Officer of the Navy'),
    ('W-2 Chief Warrant Officer 2', 'W-2 Chief Warrant Officer 2'),
    ('W-3 Chief Warrant Officer 3', 'W-3 Chief Warrant Officer 3'),
    ('W-4 Chief Warrant Officer 4', 'W-4 Chief Warrant Officer 4'),
    ('W-5 Chief Warrant Officer 5', 'W-5 Chief Warrant Officer 5'),
    ('O-1 Ensign', 'O-1 Ensign'),
    ('O-2 Lieutenant Junior Grade', 'O-2 Lieutenant Junior Grade'),
    ('O-3 Lieutenant', 'O-3 Lieutenant'),
    ('O-4 Lieutenant Commander', 'O-4 Lieutenant Commander'),
    ('O-5 Commander', 'O-5 Commander'),
    ('O-6 Captain', 'O-6 Captain'),
    ('O-7 Rear Admiral Lower Half', 'O-7 Rear Admiral Lower Half'),
    ('O-8 Rear Admiral', 'O-8 Rear Admiral'),
    ('O-9 Vice Admiral', 'O-9 Vice Admiral'),
    ('O-10 Admiral', 'O-10 Admiral'),
    ('O-11 Fleet Admiral', 'O-11 Fleet Admiral'),
    ('Other', 'Other'),
]
