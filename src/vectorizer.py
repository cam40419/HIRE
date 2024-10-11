import os
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
import Client
import json

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

            sectioned_resume = json.loads(row["Resume_json"])
            print("sectioned_resume: " + str(sectioned_resume))

            if 'resume' in sectioned_resume: 
                if 'format' in sectioned_resume['resume']:
                    sectioned_resume = sectioned_resume['resume']['format']
                else: 
                    sectioned_resume = sectioned_resume['resume']

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

                # save as csv 
                pd.DataFrame(
                    section_vector.toarray(), 
                    columns = self.tfidfvec.get_feature_names_out()
                ).to_csv(f"./vectors/{category}/{section}.csv", index=False)

    def vec_section_to_csv(self): 
        aggregated_data = {}
        for category in os.listdir("./vectors"):
            category_path = f"./vectors/{category}"

            if os.path.isdir(category_path):
                section_data = {}

                for section in os.listdir(category_path):
                    section_path = os.path.join(category_path, section)

                    if section.endswith(".csv"):
                        section_df = pd.read_csv(section_path)
                        section_data[section[:-4]] = section_df # get name of section 

                aggregated_data[category] = section_data 

        final_df = pd.DataFrame() 
        
        for category, sections in aggregated_data.items(): 
            job_data = {"Job type": category}

            for section_name, section_df in sections.items(): 
                vectors = section_df.sum(axis=0)
                job_data[section_name] = vectors.values 

            final_df = final_df.append(job_data, ignore_index = True)

        final_df.to_csv("./vectors/agg_vector.csv")

        print("Saved vector")



    def get_vec_csv(self, category, section):
        return pd.read_csv(f"./vectors/{category}/{section}.csv") 
    

vec = Vectorizer("resume.csv")
vec.process_resumes()
vec.get_vec_csv("HR", "languages")
vec.vec_section_to_csv()
