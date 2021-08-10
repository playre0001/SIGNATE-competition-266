CSV_HEADER_TYPE={
    "id"                    :"INT",
    "accommodates"          :"INT",
    "amenities"             :"STR",
    "bathrooms"             :"FLOAT",
    "bed_type"              :"STR",
    "bedrooms"              :"FLOAT",
    "beds"                  :"FLOAT",
    "cancellation_policy"   :"CATEGORY",
    "city"                  :"CATEGORY",
    "cleaning_fee"          :"BOOL",
    "description"           :"STR",
    "first_review"          :"DATE",
    "host_has_profile_pic"  :"BOOL",
    "host_identity_verified":"BOOL",
    "host_response_rate"    :"PERCENT",
    "host_since"            :"DATE",
    "instant_bookable"      :"BOOL",
    "last_review"           :"DATE",
    "latitude"              :"FLOAT",
    "longitude"             :"FLOAT",
    "name"                  :"STR",
    "neighbourhood"         :"STR",
    "number_of_reviews"     :"INT",
    "property_type"         :"CATEGORY",
    "review_scores_rating"  :"FLOAT",
    "room_type"             :"CATEGORY",
    "thumbnail_url"         :"IMAGEURL",
    "zipcode"               :"INT",
    "y"                     :"ANSWER"
}

STR_HEADER=[x for x in CSV_HEADER_TYPE.keys() if CSV_HEADER_TYPE[x]=="STR"]
STR_HEADER.remove("amenities")

CATEGORY_HEADER=[x for x in CSV_HEADER_TYPE.keys() if CSV_HEADER_TYPE[x]=="CATEGORY"]
CATEGORY_HEADER.append("amenities")

IMAGE_HEADER=[x for x in CSV_HEADER_TYPE.keys() if CSV_HEADER_TYPE[x]=="IMAGEURL"]

NUMBER_HEADER=[x for x in CSV_HEADER_TYPE.keys() if CSV_HEADER_TYPE[x]=="INT" or CSV_HEADER_TYPE[x]=="FLOAT" or CSV_HEADER_TYPE[x]=="BOOL" or CSV_HEADER_TYPE[x]=="DATE"]

MODEL_SAVE_PATH="Models"
OUTPUT_PATH="Outputs"

VALIDATION_SPLIT=0.2