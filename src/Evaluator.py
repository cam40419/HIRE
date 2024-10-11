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
# cosine_similarity_for_section(self, uploaded_vector, dataset_vectors)
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

        self.uploaded_resume_vector = self.resume_obj_to_vector(uploaded_resume_obj)
        self.dataset_vectors = self.vectorizer.get_vectors(job_category)

        self.section_word_freq = {}
        self.dataset_word_freq = self.vectorizer.get_word_frequencies(self.get_dataset_text(self.dataset_vectors))

        self.uploaded_resume_sections = ["summary", "skills", "work_experience", "education", "projects", "certifications", "hobbies", "languages"]
        self.scores = []
    
    def get_dataset_text(self, dataset_vectors):
        # Gets all the dataset sections for job category into text to be able to calc word frequencies
        dataset_text = ""
        for section_vectors in dataset_vectors:
            dataset_text += "".join(section_vectors.flatten())
        return dataset_text
    
    def resume_obj_to_vector(self, uploaded_resume_obj): 
        # Go section by section? - need to vectorize in the same way that we did for the dataset vectors
        tfidf_vectorizer = TfidfVectorizer()
        uploaded_resume_vector = tfidf_vectorizer.fit_transform([uploaded_resume_obj])
        return uploaded_resume_vector.toarray()

    # def get_dataset_vectors(self, job_category):
    #     # this needs to be done based on how vectorizer is set up/where the vectors are stored
    #     self.dataset_vectors = vectorizer.get_vectors(job_category)
    
    # def get_uploaded_sections(self, uploaded_sections):
    #     # TODO: This needs to be gotten so we can go through section by section
    #     self.sections = uploaded_sections


    def cosine_similarity_scores(self):
        # Reinitialize scores
        self.scores = []
        for i, dataset_vector in enumerate(self.dataset_vectors):
            similarity_score = cosine_similarity(self.uploaded_resume_vector, dataset_vector)
            self.scores[section] = cosine_similarity(self.uploaded_resume_vector[section], self.dataset_vectors[section])
        return self.scores
    
    def generate_overall_score(self):
        if self.scores == []:
            return None
        return (np.mean(self.scores) * 100)
    
    def evaluate_section_word_frequencies(self, section_name, section_content):
        """
        Compare word frequencies of a section from the uploaded resume to the dataset.
        Detect overused or underused words.
        """
        uploaded_word_freq = self.vectorizer.get_word_frequencies(section_content)
        overused_words = []
        underused_words = []
        
        for word, freq in uploaded_word_freq.items():
            dataset_avg_freq = self.dataset_word_freq.get(word, 0)
            if freq > dataset_avg_freq * 1.5:  # Consider overused if 50% more frequent
                overused_words.append(word)
            elif freq < dataset_avg_freq * 0.5:  # Consider underused if 50% less frequent
                underused_words.append(word)

        return overused_words, underused_words
    
    # def generate_section_feedback(self, score, keywords):
    #     return generate_feedback()

    def evaluate_section(self, section_name, section_content):
        uploaded_vector = self.resume_section_to_vector(section_content)
        dataset_vectors = self.dataset_vectors  # Get relevant dataset vectors
        similarity_score = self.cosine_similarity_for_section(uploaded_vector, dataset_vectors)
        return similarity_score

    def evaluate(self):
        scores = self.cosine_similarity_scores()
        best_score_idx = np.argmax(scores)
        return scores[0][best_score_idx], best_score_idx
    
    def evaluate2(self):
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
                "underused_words": underused
            }

        return self.scores, self.section_feedback
