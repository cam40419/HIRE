import os
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
import Client

# Methods:
# __init__
# process_resumes(self)
# get_word_frequencies(self, text)
# get_vec_csv(self, category, section)
# get_vectors(self, category)

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
    # def get_word_frequencies(self, category):
    #     word_frequencies = {}
    #     vector_dir = f"./vectors/{category}"
        
    #     if os.path.exists(vector_dir):
    #         for file_name in os.listdir(vector_dir):
    #             if file_name.endswith("_freq.csv"):  # Fetch word frequency files
    #                 section_freq = pd.read_csv(os.path.join(vector_dir, file_name))
    #                 for _, row in section_freq.iterrows():
    #                     word = row['word']
    #                     freq = row['frequency']
    #                     if word in word_frequencies:
    #                         word_frequencies[word] += freq
    #                     else:
    #                         word_frequencies[word] = freq

    #     # Normalize the word frequencies
    #     total_word_count = sum(word_frequencies.values())
    #     word_frequencies = {word: freq / total_word_count for word, freq in word_frequencies.items()}
    #     return word_frequencies



    def get_vec_csv(self, category, section):
        return pd.read_csv(f"./vectors/{category}/{section}.csv") 
    
    # Getting vectors for the categorty as a whole (May or may not be used)
    def get_vectors(self, category):
        vectors = []
        vector_dir = f"./vectors/{category}"
        if os.path.exists(vector_dir):
            for file_name in os.listdir(vector_dir):
                if file_name.endswith(".csv"):
                    section_vectors = pd.read_csv(os.path.join(vector_dir, file_name))
                    vectors.append(section_vectors.values)
        return vectors

vec = Vectorizer("resume2.csv")
vec.process_resumes()
vec.get_vec_csv("HR", "languages")
