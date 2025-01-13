import json

import pandas as pd
from sphinx.search import languages


class FewShotPost:
    def __init__(self,file_path = "data/processed_post.json"):
        self.df = None
        self.unique_tags = None
        self.load_post(file_path)


    def load_post(self,file_path):
        with open(file_path, encoding="utf-8") as f:
            posts =json.load(f)
            self.df =pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            all_tags = self.df["tags"].apply(lambda x : x).sum()
            self.unique_tags = set(list(all_tags))

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif line_count <= 5 <= 10:
            return "Medium"
        elif line_count > 10:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['length'] == length)&
            (self.df['language'] == language) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]

        return df_filtered.to_dict(orient = "records")



if __name__ == "__main__":
    fs =FewShotPost()
    posts = fs.get_filtered_posts("Short","English","Job Search")
    print(posts)