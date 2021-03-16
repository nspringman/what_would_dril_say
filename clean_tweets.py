import pandas as pd
import re
import numpy as np

if __name__ == "__main__":
    tw = pd.read_csv('data/driltweets.csv', usecols=['content'])
    reg = re.compile(r"(pic.twitter.com\/[a-zA-Z0-9]{10})|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))")
    tw['content'] = [reg.sub('',x) for x in tw['content']]
    tw['content'].replace('',np.nan,inplace=True)
    tw.dropna(subset=['content'],inplace=True)
    tw.to_csv('data/cleaned_tweets.csv', index=False)