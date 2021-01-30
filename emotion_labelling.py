import helpers
import dataset as ds
from nltk.stem.porter import *

stemmer = PorterStemmer()

lexicon = helpers.load_dataset("nrc_emotion_lexicon.csv")

# stemming()
# parameters:
#   word : string - the word to be stemmed
# returns:
#   word : string - the stemmed version of the word
# description:
#   This function stems a word using the NLTK Porter Stemmer and changes stemmed
#       words ending with 'i' to end with 'y' for compatibility with WordNet.
def stemming (word):
    global stemmer
    word = str(word)
    word = stemmer.stem(word)
    if word.endswith('i'):
        word = word[:-1]
        word = word + 'y'
    return word

word_list = lexicon.Word.tolist()
stemmed_word_list = []
new_word_list = []

for word in word_list:
    word = str(word)
    new_word_list.append(word)
    stemmed_word_list.append(stemming(word))

word_list = new_word_list


# match_checker()
# parameters:
#   word : string - the word to be checked
# returns:
#   [] : list - list containing the number of matches for each emotion [OR]
#   None : None - None
# description:
#   This function checks for matches between a given word and the NRC lexicon,
#       and returns the natches for each emotion (or None).
def match_checker (word):
    global lexicon, word_list, stemmed_word_list
    if word in word_list or stemming(word) in stemmed_word_list:
        lex_slice = lexicon[(lexicon.Word == word) | (lexicon.Word == stemming(word))]
        if len(lex_slice) == 0:
            for index, row in lexicon.iterrows():
                if word == row.Word or stemming(word) == stemming(row.Word):
                    return [row.Anger, row.Anticipation, row.Disgust, row.Fear, row.Joy, row.Sadness, row.Surprise, row.Trust]
        else:
            for index, row in lex_slice.iterrows():
                return [row.Anger, row.Anticipation, row.Disgust, row.Fear, row.Joy, row.Sadness, row.Surprise, row.Trust]
    return None


df = helpers.load_dataset(ds.output_data + "rt_removed_unlabelled.csv")

emotion_list = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
for emotion in emotion_list:
    df[emotion] = 0
df["lexicon_matches"] = 0
df["total_words"] = 0



for index, row in df.iterrows():
    print(index)
    match_data = {}
    for emotion in emotion_list:
        match_data[emotion] = 0
    lexicon_matches = 0
    for word in row.preprocessed_tweet_text.split():
        word = str(word)
        word_match_data = match_checker(word)
        if word_match_data != None:
            lexicon_matches += 1
            for emotion, data in zip(emotion_list, word_match_data):
                match_data[emotion] += data
    df.anger.at[index] = match_data["anger"]
    df.anticipation.at[index] = match_data["anticipation"]
    df.disgust.at[index] = match_data["disgust"]
    df.fear.at[index] = match_data["fear"]
    df.joy.at[index] = match_data["joy"]
    df.sadness.at[index] = match_data["sadness"]
    df.surprise.at[index] = match_data["surprise"]
    df.trust.at[index] = match_data["trust"]
    df.lexicon_matches.at[index] = lexicon_matches
    df.total_words.at[index] = len(row.preprocessed_tweet_text.split())

helpers.dataframe_to_csv(df, ds.output_data + "nrc_labelled.csv")
