# Create evaluator class for resume scoring
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Vectorizer
import numpy as np

# Methods:
# __init__
# get_dataset_text(self)
# evaluate_section(self, section_name, section_content)
# resume_section_to_vector(self, section_text)
# cosine_similarity_section_score(self, uploaded_vector, dataset_vectors)
# evaluate_section_word_frequencies(self, section_name, section_content)
# generate_section_feedback(self, section_name, score)
# evaluate(self)

class Evaluator:
    def __init__(self, job_category, uploaded_resume_obj):
        # Vectorizer object initialized with the resume database
        self.vectorizer = Vectorizer.Vectorizer("resume2.csv")
        self.vectorizer.process_resumes()

        self.job_category = job_category
        self.uploaded_resume_obj = uploaded_resume_obj 
        # Assume that the uploaded resume has already been split into sections

        self.uploaded_resume_sections = ["summary", "skills", "work_experience", "education", "projects", "certifications", "hobbies", "languages"]
        self.scores = []
    
    def get_dataset_text(self, dataset_vectors):
        # Gets all the dataset sections for job category into text to be able to calc word frequencies
        dataset_text = ""
        for section_vectors in dataset_vectors:
            dataset_text += "".join(section_vectors.flatten())
        return dataset_text
    
    def resume_section_to_vector(self, uploaded_resume_section): 
        # Go section by section - Assuming that the resume object has already been broken up into sections
        tfidf_vectorizer = TfidfVectorizer()
        section_vector = tfidf_vectorizer.fit_transform([uploaded_resume_section])
        return section_vector.toarray()

    def cosine_similarity_section_score(self, uploaded_vector, dataset_vectors):
        similarities = []
        for dataset_vector in dataset_vectors:
            similarity_score = cosine_similarity(uploaded_vector, dataset_vector)
            similarities.append(similarity_score.mean())
        return np.mean(similarities)
    
    def evaluate_section(self, section_name, section_text):
        # Gets the vector of the uploaded resume and the vectors from section from the dataset and returns cosine_sim score
        uploaded_vector = self.resume_section_to_vector(section_text)
        dataset_section_vectors = self.vectorizer.get_vec_csv(self.job_category, section_name)

        section_score = self.cosine_similarity_section_score(uploaded_vector, dataset_section_vectors)
        return section_score
    
    # def generate_overall_score(self):
    #     if self.scores == []:
    #         return None
    #     return (np.mean(self.scores) * 100)
    
    def evaluate_section_word_frequencies(self, section_name, section_text):
        # Gets word frequencies for the uploaded resume section
        uploaded_word_freq = self.vectorizer.get_word_frequencies(section_text)
        overused_words = []
        underused_words = []

        # Get word frequencies from current section from dataset
        dataset_word_vector = self.vectorizer.get_vec_csv(self.job_category, section_name)
        dataset_word_freq = self.vectorizer.get_word_frequencies(self.get_dataset_text(dataset_word_vector))
        
        # Compare word frequencies in uploaded section and dataset
        for word, freq in uploaded_word_freq.items():
            dataset_avg_freq = dataset_word_freq.get(word, 0)
            if freq > dataset_avg_freq * 1.5:  # Consider overused if 50% more frequent
                overused_words.append(word)
            elif freq < dataset_avg_freq * 0.5:  # Consider underused if 50% less frequent
                underused_words.append(word)

        return overused_words, underused_words
    
    def generate_section_feedback(self, score, section_name):
        if score > 0.8:
            return f"Section '{section_name}': Excellent match!"
        elif 0.6 <= score <= 0.8:
            return f"Section '{section_name}': Good match, but can be improved."
        else:
            return f"Section '{section_name}': Needs improvement."

    def evaluate_section(self, section_name, section_content):
        uploaded_vector = self.resume_section_to_vector(section_content)
        dataset_vectors = self.dataset_vectors  # Get relevant dataset vectors
        similarity_score = self.cosine_similarity_section_score(uploaded_vector, dataset_vectors)
        return similarity_score
    
    def evaluate(self):
        # Regular section-wise evaluation (similarity) code remains the same
        for section_name, section_content in self.uploaded_resume_sections.items():
            # Evaluate cosine similarity
            score = self.evaluate_section(section_name, section_content)
            self.scores[section_name] = score
            
            # Generate feedback for over/underused words
            overused, underused = self.evaluate_section_word_frequencies(section_name, section_content)
            self.section_feedback[section_name] = {
                "similarity_score": score,
                "overused_words": overused,
                "underused_words": underused,
                "feedback": self.generate_section_feedback(score, section_name)
            }

        return self.scores, self.section_feedback
