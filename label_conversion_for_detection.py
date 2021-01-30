import helpers
import dataset as ds

df = helpers.load_dataset(ds.output_data + "nrc_labelled.csv")

for emotion in ds.emotion_list:
    emotion_str = emotion + "_str"
    df[emotion_str] = ""

for index, row in df.iterrows():
    for emotion in ds.emotion_list:
        emotion_str = emotion + "_str"
        if row[emotion] == 0:
            df[emotion_str].at[index] = "no_" + emotion

        else:
            df[emotion_str].at[index] = emotion

helpers.dataframe_to_csv(df, ds.output_data + "nrc_labelled_for_detection.csv")
print(df)
