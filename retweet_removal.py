import helpers
import dataset as ds

df = helpers.load_dataset(ds.dataset + ds.data)

new_df = df[df.is_retweet == False]
helpers.dataframe_to_csv(new_df, ds.output_data + "rt_removed_unlabelled.csv")
