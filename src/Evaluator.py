# Create evaluator class for resume scoring
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Vectorizer

class Evaluator:
    vectorizer = Vectorizer.Vectorizer()

    sections = None


    def __init__(self, dataset_resumes, dataset_vectors, uploaded_resume_vector):
        """
        Evaluator class to compare uploaded resumes to dataset resumes.
        :param dataset_resumes: The list of Resume objects in the dataset.
        :param dataset_vectors: The TF-IDF vectors for each section based on related dataset resumes.
        :param uploaded_resume_vector: The TF-IDF vector of the uploaded resume.
        """
        self.dataset_resumes = dataset_resumes # Needed by the feedback function
        self.dataset_vectors = dataset_vectors
        self.uploaded_resume_vector = uploaded_resume_vector
    
    # Only needed if the uploaded resume is not already in vector form?
    # def resume_obj_to_vector(self): 
    #     return TfidfVectorizer()
    def get_dataset_vectors(self, job_description):
        """
        Gets the section vectors from the dataset based on the job description  
        """
        # TODO: this needs to be done based on how vectorizer is set up/where the vectors are stored
        self.dataset_vectors = vectorizer.get_vectors(job_description)
    
    def get_uploaded_sections(self, uploaded_sections):
        """
        Gets the section titles from the uploaded resume
        """
        self.sections = uploaded_sections

    def cosine_similarity_scores(self):
        """
        Calculate cosine similarity between the uploaded resume and dataset.
        :return: Cosine similarity scores.
        """
        return cosine_similarity(self.uploaded_resume_vector, self.dataset_vectors)
    
    def generate_overall_score(self):
        return None
    
    def generate_section_feedback(self, score, keywords):
        """
        Generates feedback based on simalarity score for a certain section
        :return text feedback for given resume section
        """
        return generate_feedback()

    def evaluate(self):
        """
        Evaluate the uploaded resume by comparing it to the dataset.
        :return: A tuple containing the highest similarity score and index of the best match.
        """
        scores = self.cosine_similarity_scores()
        best_score_idx = np.argmax(scores)
        return scores[0][best_score_idx], best_score_idx


# Notes for my own benefit
"""
This class is given the assumption that the words have been transformed into vectors already (by the vectorizer class)
this is a good explanation for the TF-IDF thing: https://medium.com/@imamun/creating-a-tf-idf-in-python-e43f05e4d424 

They need to be split up the same way for the cosine similarity to be meaningful

In order to return feedback we also need to know the Words with frequency - based on the job category
TODO: Need to get that somehow - should we be given the wordlist? or just give generic feedback to 
return the top 3 or something similar?


"""