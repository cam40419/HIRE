# Create evaluator class for resume scoring
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Vectorizer
import numpy as np

class Evaluator:
    def __init__(self, job_description, uploaded_resume_obj):
        self.vectorizer = Vectorizer.Vectorizer() #?
        self.job_description = job_description
        self.uploaded_resume_obj = uploaded_resume_obj # Needed?

        self.uploaded_resume_vector = self.resume_obj_to_vector(uploaded_resume_obj)
        self.dataset_vectors = self.vectorizer.get_dataset_vectors(job_description)
        self.sections = None # needed to give feedback to each of the sections in uploaded res_obj 
        self.scores = []
    
    def resume_obj_to_vector(self): 
        # Go section by section? - need to vectorize in the same way that we did for the dataset vectors
        return TfidfVectorizer(self.uploaded_resume_obj)

    def get_dataset_vectors(self, job_description):
        # TODO: this needs to be done based on how vectorizer is set up/where the vectors are stored
        self.dataset_vectors = vectorizer.get_vectors(job_description)
    
    def get_uploaded_sections(self, uploaded_sections):
        self.sections = uploaded_sections

    def cosine_similarity_scores(self):
        for section in sections:
            self.scores[section] = cosine_similarity(self.uploaded_resume_vector[section], self.dataset_vectors[section])
        return self.scores
    
    def generate_overall_score(self):
        if self.scores == []:
            return None
        return (np.mean(self.scores) * 100)
    
    def generate_section_feedback(self, score, keywords):
        return generate_feedback()

    def evaluate(self):
        scores = self.cosine_similarity_scores()
        best_score_idx = np.argmax(scores)
        return scores[0][best_score_idx], best_score_idx
