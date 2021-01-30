import helpers
import dataset as ds
import pandas as pd

emotion_list = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
counter = {}
for emotion in emotion_list:
    counter[emotion] = 0
counter["no_emotion"] = 0
counter["no_lexicon_matches"] = 0

df = helpers.load_dataset(ds.output_data + "nrc_labelled.csv")
print(len(df))

for index, row in df.iterrows():
    zero_emotion = 0
    for emotion in emotion_list:
        if row[emotion] != 0:
            counter[emotion] += 1
        else:
            zero_emotion += 1
    if zero_emotion == 8 and row.lexicon_matches != 0:
        counter["no_emotion"] += 1
    if row.lexicon_matches == 0:
        counter["no_lexicon_matches"] += 1



temp_list = []
for emotion in counter:
    temp_list.append([emotion, counter[emotion]])

cols = ["emotion", "count"]

emo_df = pd.DataFrame(temp_list, columns=cols)

emo_df = emo_df.sort_values(by=['count'], ascending=False)
print(emo_df)

helpers.dataframe_to_csv(emo_df, ds.output_data + "emotion_counts.csv")
