

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



#school_type
SCHOOL_TYPE_CHOICES = (
    ('elementary', 'Elementary School'),
    ('middle', 'Middle School'),
    ('high', 'High School'),
    ('college', 'College/University'),
    ('other', 'Other'),
)

#DEGREE_TYPE
DEGREE_TYPE_CHOICES = (
    ('associate_of_arts', 'Associate of Arts (A.A.)'),
    ('associate_of_science', 'Associate of Science (A.S.)'),
    ('associate_of_applied_science', 'Associate of Applied Science (A.A.S.)'),
    ('associates_degree_in_nursing', 'Associates Degree in Nursing (ADN)'),
    ('bachelor_of_arts', 'Bachelor of Arts (B.A.)'),
    ('bachelor_of_science', 'Bachelor of Science (B.S.)'),
    ('bachelor_of_fine_arts', 'Bachelor of Fine Arts (BFA)'),
    ('bachelor_of_business_administration', 'Bachelor of Business Administration (BBA)'),
    ('bachelor_of_engineering', 'Bachelor of Engineering (B.E.)'),
    ('bachelor_of_architecture', 'Bachelor of Architecture (B.Arch)'),
    ('bachelor_of_music', 'Bachelor of Music (B.M.)'),
    ('doctor_of_medicine', 'Doctor of Medicine (M.D.)'),
    ('doctor_of_dental_surgery', 'Doctor of Dental Surgery (D.D.S.)'),
    ('doctor_of_pharmacy', 'Doctor of Pharmacy (Pharm.D.)'),
    ('doctor_of_veterinary_medicine', 'Doctor of Veterinary Medicine (D.V.M.)'),
    ('doctor_of_osteopathic_medicine', 'Doctor of Osteopathic Medicine (D.O.)'),
    ('doctor_of_nursing_practice', 'Doctor of Nursing Practice (DNP)'),
    ('doctor_of_philosophy', 'Doctor of Philosophy (Ph.D.)'),
    ('juris_doctor', 'Juris Doctor (J.D.)'),
    ('master_of_arts', 'Master of Arts (M.A.)'),
    ('master_of_science', 'Master of Science (M.S.)'),
    ('master_of_business_administration', 'Master of Business Administration (MBA)'),
    ('master_of_public_administration', 'Master of Public Administration (MPA)'),
    ('master_of_fine_arts', 'Master of Fine Arts (MFA)'),
    ('master_of_education', 'Master of Education (M.Ed.)'),
    ('master_of_social_work', 'Master of Social Work (MSW)'),
    ('master_of_architecture', 'Master of Architecture (M.Arch)'),
    ('master_of_music', 'Master of Music (M.M.)'),
    ('master_of_health_administration', 'Master of Health Administration (MHA)'),
    ('master_of_information_science', 'Master of Information Science (MIS)'),
    ('doctor_of_education', 'Doctor of Education (Ed.D.)'),
    ('doctor_of_psychology', 'Doctor of Psychology (Psy.D.)'),
    ('doctor_of_social_work', 'Doctor of Social Work (DSW)'),
    ('none', 'None'),
)

#CERTIFICATION_LICENSES
CERTIFICATION_LICENSES=(
    ('CERTIFICATION', 'CERTIFICATION'),
    ('LICENSES', 'LICENSES'),
)
#SALARY_TYPES
SALARY_TYPES = (
        ('annual', 'Annual Salary'),
        ('monthly', 'Monthly Salary'),
        ('twoWeeks', 'Two Weeks Salary'),
        ('weekly', 'Weekly Salary'),
        ('daily', 'Daily Rate'),
        ('hourly', 'Hourly Wage'),
        ('commission', 'Commission'),
        ('bonus', 'Bonus'),
        ('profit_sharing', 'Profit Sharing'),
        ('other', 'Other'),
    )

#JOB_TYPES
JOB_TYPES = (
        ('', 'Select Job Type'),  # Provide an empty option
        ('Temporary', 'Temporary'),
        ('Temp-Perm', 'Temporary to Permanent'),
        ('Permanent', 'Permanent'),
        # ('full-time', 'Full-time'),
        # ('part-time', 'Part-time'),
        # ('contract', 'Contract/Freelance'),
        # ('internship', 'Internship'),
        # ('apprenticeship', 'Apprenticeship'),
        # ('remote', 'Remote/Telecommute'),
        # ('shift-based', 'Shift-based'),
        # ('consultant', 'Consultant'),
        # ('other', 'Other'),
)

SORT_CHOICES = (
        ('', 'Sort by'),
        ('newest', 'Newly Posted'),
        # Add more sorting choices here as needed
)
# Location preference choices
LOCATION_CHOICES = [
        ('home_proximity', 'Proximity to Home/Family'),
        ('job_opportunity', 'Job Market and Opportunities'),
    ]
#Work arrangement choices
WORK_ARRANGEMENT_CHOICES = [
        ('', 'Select Work Arrangement Preference'),  # Provide an empty option
        ('REMOTE', 'Remote'),
        ('ON_SITE', 'On-site'),
        ('HYBRID', 'Hybrid'),
    ]
#RELOCATION
RELOCATION = (('Yes', 'Yes'),('No', 'No'),)

#skill
TEST_STATES = (
        ('in-progress', 'In Progress'),
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('skipped', 'Skipped'),
        ('started', 'Started'),
        
    )

#retting
TAG_CHOOSES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('good', 'good'),
        ('bast', 'bast'),
        ('qualified', 'qualified'),
        
    )

#VIDEO 
VIDEO_STATES_CHOOSES=(
    ('InProgress', 'InProgress'),
    ('pending', 'pending'),
    ('activated', 'activated'),
)

BACKGROUND_CHECK_CHOOSES_STATES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
)

CARD_TYPE_CHOOSE=(
    ("master-card", "Master-card"),
    ("visa", "Visa"),
)

RIDE_CHOOSE=(
        ('UberRide', 'Uber Ride'),
        ('LyftRide', 'Lyft Ride'),
    )

# Choices for the 'taxUserType' field
TAX_USER_TYPE_CHOICES = (
    ('employee', 'Employee'),
    ('contractor', 'Contractor/Freelancer'),
)

# Choices for the 'formType' field
FORM_TYPE_CHOICES = (
    ('w-4', 'W-4'),
    ('w-9', 'W-9'),
)

# Choices for the 'states' field
DOCUMENT_STATES_CHOICES = (
    ('valid', 'Valid'),
    ('invalid', 'Invalid'),
    ('pending', 'Pending'),
)

#JobRequisition
ACTION_TYPES = (
        ('SAVE', 'Save'),
        ('ALERT', 'Alert'),
        ('POST', 'Post'),
        ('ALL', 'All'),
    )

#AppliedJobHistory
STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('in_cart', 'In Cart'),
        ('message', 'Message'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
#TIME_CARD_DATE_ASSIGN
DATE_ASSIGN = [
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
]

#TimeCard
TIME_CARD_STATUS =[
    ('accepted','accepted'),
    ('rejected','rejected'),
    ('panging','panging'),
    ('complete','complete'),
]

TARGET_AUDIENCE  = (('employee', 'employee'),('employer', 'employer'),)