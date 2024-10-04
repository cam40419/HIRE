from typing import List, Optional


class ContactDetails:
    def __init__(self, email: str = "", phone: str = "", address: str = "", linkedin: str = "", github: str = "", website: str = ""):
        self.email = email
        self.phone = phone
        self.address = address
        self.linkedin = linkedin
        self.github = github
        self.website = website


class Skill:
    def __init__(self, name: str = "", proficiency: str = ""):
        self.name = name
        self.proficiency = proficiency


class WorkExperience:
    def __init__(self, company: str = "", job_title: str = "", location: str = "", start_date: str = "", end_date: str = "", responsibilities: Optional[List[str]] = None):
        if responsibilities is None:
            responsibilities = []
        self.company = company
        self.job_title = job_title
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.responsibilities = responsibilities


class Education:
    def __init__(self, institution: str = "", degree: str = "", field_of_study: str = "", start_date: str = "", end_date: str = "", gpa: Optional[float] = None):
        self.institution = institution
        self.degree = degree
        self.field_of_study = field_of_study
        self.start_date = start_date
        self.end_date = end_date
        self.gpa = gpa


class Project:
    def __init__(self, title: str = "", description: str = "", technologies_used: Optional[List[str]] = None, start_date: str = "", end_date: str = "", github_link: str = "", live_demo: str = ""):
        if technologies_used is None:
            technologies_used = []
        self.title = title
        self.description = description
        self.technologies_used = technologies_used
        self.start_date = start_date
        self.end_date = end_date
        self.github_link = github_link
        self.live_demo = live_demo


class Certification:
    def __init__(self, name: str = "", issuing_organization: str = "", issue_date: str = "", expiration_date: str = "", credential_id: str = "", credential_url: str = ""):
        self.name = name
        self.issuing_organization = issuing_organization
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.credential_id = credential_id
        self.credential_url = credential_url


from typing import List, Optional
import json

# Existing classes (ContactDetails, Skill, WorkExperience, etc.) would go here...

class Resume:
    def __init__(self, name: str = "", age: Optional[int] = None, contact_details: ContactDetails = None, summary: str = "", skills: Optional[List[Skill]] = None, work_experience: Optional[List[WorkExperience]] = None, education: Optional[List[Education]] = None, projects: Optional[List[Project]] = None, certifications: Optional[List[Certification]] = None, hobbies: Optional[List[str]] = None, languages: Optional[List[str]] = None):
        if contact_details is None:
            contact_details = ContactDetails()
        if skills is None:
            skills = []
        if work_experience is None:
            work_experience = []
        if education is None:
            education = []
        if projects is None:
            projects = []
        if certifications is None:
            certifications = []
        if hobbies is None:
            hobbies = []
        if languages is None:
            languages = []
        
        self.name = name
        self.age = age
        self.contact_details = contact_details
        self.summary = summary
        self.skills = skills
        self.work_experience = work_experience
        self.education = education
        self.projects = projects
        self.certifications = certifications
        self.hobbies = hobbies
        self.languages = languages

    @classmethod
    def from_json(cls, data: dict) -> 'Resume':
        # Parse contact details
        contact_details_data = data.get("contact_details", {})
        contact_details = ContactDetails(
            email=contact_details_data.get("email", ""),
            phone=contact_details_data.get("phone", ""),
            address=contact_details_data.get("address", ""),
            linkedin=contact_details_data.get("linkedin", ""),
            github=contact_details_data.get("github", ""),
            website=contact_details_data.get("website", "")
        )

        # Parse skills
        skills_data = data.get("skills", [])
        skills = [Skill(name=skill.get("name", ""), proficiency=skill.get("proficiency", "")) for skill in skills_data]

        # Parse work experience
        work_experience_data = data.get("work_experience", [])
        work_experience = [
            WorkExperience(
                company=job.get("company", ""),
                job_title=job.get("job_title", ""),
                location=job.get("location", ""),
                start_date=job.get("start_date", ""),
                end_date=job.get("end_date", ""),
                responsibilities=job.get("responsibilities", [""])
            ) for job in work_experience_data
        ]

        # Parse education
        education_data = data.get("education", [])
        education = [
            Education(
                institution=edu.get("institution", ""),
                degree=edu.get("degree", ""),
                field_of_study=edu.get("field_of_study", ""),
                start_date=edu.get("start_date", ""),
                end_date=edu.get("end_date", ""),
                gpa=edu.get("gpa", None)
            ) for edu in education_data
        ]

        # Parse projects
        projects_data = data.get("projects", [])
        projects = [
            Project(
                title=project.get("title", ""),
                description=project.get("description", ""),
                technologies_used=project.get("technologies_used", []),
                start_date=project.get("start_date", ""),
                end_date=project.get("end_date", ""),
                github_link=project.get("github_link", ""),
                live_demo=project.get("live_demo", "")
            ) for project in projects_data
        ]

        # Parse certifications
        certifications_data = data.get("certifications", [])
        certifications = [
            Certification(
                name=cert.get("name", ""),
                issuing_organization=cert.get("issuing_organization", ""),
                issue_date=cert.get("issue_date", ""),
                expiration_date=cert.get("expiration_date", ""),
                credential_id=cert.get("credential_id", ""),
                credential_url=cert.get("credential_url", "")
            ) for cert in certifications_data
        ]

        # Parse hobbies and languages
        hobbies = data.get("hobbies", [])
        languages = data.get("languages", [])

        # Create Resume instance
        return cls(
            name=data.get("name", ""),
            age=data.get("age", None),
            contact_details=contact_details,
            summary=data.get("summary", ""),
            skills=skills,
            work_experience=work_experience,
            education=education,
            projects=projects,
            certifications=certifications,
            hobbies=hobbies,
            languages=languages
        )
