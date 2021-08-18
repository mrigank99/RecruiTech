from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from basic import *
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import time

def get_recommendation(top, df_all, scores,u_id):
  recommendation = pd.DataFrame(columns = ['ApplicantID', 'JobID',  'title', 'score'])
  count = 0
  for i in top:
      recommendation.at[count, 'ApplicantID'] = u_id
      recommendation.at[count, 'JobID'] = df_all['Job.ID'][i]
      recommendation.at[count, 'title'] = df_all['Title'][i]
      recommendation.at[count, 'score'] =  scores[count]
      count += 1
  return recommendation


def get_job_recommendations(userId):
    skills = candidateSkills.query.with_entities(candidateSkills.technical,candidateSkills.interpersonal).filter_by(cid=userId).first() \
        if candidateSkills.query.with_entities(candidateSkills.technical,candidateSkills.interpersonal).filter_by(cid=userId).first() is not None else [""]
    # Format of skills which will be returned [(Tech,Interp), (4,), (5,)]

    education = candidateEducation.query.with_entities(candidateEducation.degree_level).filter_by(cid=userId).first() \
        if candidateEducation.query.with_entities(candidateEducation.degree_level).filter_by(cid=userId).first() is not None else [""]

    experience = candidateExperience.query.with_entities(candidateExperience.department,candidateExperience.about_role).filter_by(cid=userId).first() \
        if candidateExperience.query.with_entities(candidateExperience.department,candidateExperience.about_role).filter_by(cid=userId).first() is not None else [""]

    preferance = candidateDetails.query.with_entities(candidateDetails.preference).filter_by(cid=userId).first() \
        if candidateDetails.query.with_entities(candidateDetails.preference).filter_by(cid=userId).first() is not None else [""]

    Text = skills[0]+education[0]+experience[0]+preferance[0]
    finalUserText=[]
    finalUserText.append(Text)
    # for job in jobList:
    #     finaltext = ""
    #     if job.jobName is not None:
    #         finaltext += job.jobName
    #     if job.department is not None:
    #         finaltext += job.department
    #     if job.skills is not None:
    #         finaltext += job.skills
    #     if job.qualifications is not None:
    #         finaltext += job.qualifications
    #     if job.jobdescription is not None:
    #         finaltext += job.jobdescription
    #     if job.requirements is not None:
    #         finaltext += job.requirements
    #
    #     df = df.append({'finalText': finaltext},
    #                    ignore_index=True)

    #We can not use our jobs as we have less jobs in database

    df_thirty = pickle.load(open("df_thirty", "rb"))
    tfidf_vectorizer = pickle.load(open("fitted_vect.pickle", "rb"))
    tfidf_jobid_thirty = pickle.load(open("tfidf_jobid_thirty.pickle", "rb"))

    user_tfidf = tfidf_vectorizer.transform(finalUserText)

    cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x), tfidf_jobid_thirty)
    current = time.time()
    output2 = list(cos_similarity_tfidf)  # Calculating output2 based on calculated cos-similarity
    final = time.time()
    timeTaken = final - current
    timeTaken

    print("matrix:",user_tfidf)
    print("Time taken: ", timeTaken)

    top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
    list_scores = [output2[i][0][0] for i in top]
    result = get_recommendation(top, df_thirty, list_scores,u_id=userId)
    result.to_csv('Recomendations.csv')
    # print(finalUserText)
    # print(tfidf_matrix_jobs.shape)
    # print(tfidf_matrix_user.shape)
    # cosine_sim = linear_kernel(tfidf_matrix_user, tfidf_matrix_jobs)
    # print(cosine_sim)
    #
    # cos_similarity_tfidf = map(lambda x: cosine_similarity(tfidf_matrix_user, x), tfidf_matrix_jobs)
    # print("Similarity matrix is: ",list(cos_similarity_tfidf))

    return True

