import os
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
import Client

class Vectorizer: 

    def __init__(self, db_string): 
        self.db_string = db_string
        self.resume_db = pd.read_csv(db_string)
        self.category_dict = dict() 
        self.cc = Client.chat_completion(preset_name="DEFAULT")
        self.tfidfvec = TfidfVectorizer()
        self.process_resumes()
        print("Processed init")

    def process_resumes(self): 

        # iterate over rows 
        for _, row in self.resume_db.iterrows(): 
            sectioned_resume = self.cc.chat(row['Resume_str'])
            print("sectioned_resume: " + str(sectioned_resume))
            
            sectioned_resume = sectioned_resume['resume']['format']

            # check if category in dict 
            if row['Category'] not in self.category_dict: 
                self.category_dict[row['Category']] = []

            # add sectioned resume to category
            self.category_dict[row['Category']].extend(sectioned_resume)

        # vectorize 
        for category, sections in self.category_dict.items(): 

            print("sections: ", sections)
            # save to folder 
            print(f"Attempting to make directory vectors/{category}")
            os.makedirs(f"./vectors/{category}", exist_ok=True)
            print(f"Created or exists: vectors/{category}")

            for ind, section in enumerate(sections):
                print(f"Processing section: {section}") 
                if not section.strip():  # Skip empty sections
                    print(f"Skipping empty section for category {category}")
                    continue

                print(f"Section: {section}") 
                section_vector = self.tfidfvec.fit_transform([section])
                word_freq = self.get_word_frequencies([section])

                # save TF-IDF vectors as csv 
                pd.DataFrame(
                    section_vector.toarray(), 
                    columns = self.tfidfvec.get_feature_names_out()
                ).to_csv(f"./vectors/{row['Category']}/{section}.csv", index=False)

                # Save word frequencies as csv
                pd.DataFrame(
                    list(word_freq.items()), 
                    columns=["word", "frequency"]
                ).to_csv(f"./vectors/{row['Category']}/{section}_freq.csv", index=False)
    
    def get_word_frequencies(self, text):
        # Get the raw counts
        vectorizer = TfidfVectorizer(use_idf=False, norm=None) 
        word_vector = vectorizer.fit_transform([text])
        word_freq = dict(zip(vectorizer.get_feature_names_out(), word_vector.toarray()[0]))
        return word_freq

    def get_vec_csv(self, category, section):
        return pd.read_csv(f"./vectors/{category}/{section}.csv") 
    

vec = Vectorizer("resume.csv")
vec.process_resumes()
