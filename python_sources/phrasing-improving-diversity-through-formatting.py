#!/usr/bin/env python
# coding: utf-8

# <h1> Phrasing: Improving Diversity Through Formatting </h1>
# <p><strong>2019-6-18</strong><ol>
# <a href="https://ibb.co/SyxPRHx"><img src="https://i.ibb.co/YQW3pJW/diversity.jpg" alt="diversity" border="0"></a>
# *Credit: Shutterstock*
# <li> <a href="#intro">A Brief Anecdote</a></li>
# <li> <a href="#prepa">Data Preparation</a>
#     <ol>
#     <li> <a href="#metho">Methodology and Runtime Analysis</a> </li>
#     <li> <a href="#evalu">Evaluation and Areas of Improvement</a> </li>
#     <li> <a href="#store">Data Storage Recommendations</a> </li>
#     </ol></li>
# <li><a href="#demog">Job Demographics: Salaries, Word Count, and Gendered Language</a> 
#     <ol>
#     <li> <a href="#salar">Salaries</a> </li>
#     <li> <a href="#count">Word Count</a> </li>
#     <li> <a href="#gende">Gendered Language</a> </li> 
#     </ol></li>
# <li><a href="#forma">Actionable Formatting Improvements</a>
#     <ol>
#     <li> <a href="#cut">Cut Word Count and Reading Level</a> </li>
#     <li> <a href="#clari">Clarify Salary Expectations and Progression</a> </li>
#     <li> <a href="#cleans">Cleanse Excessive Certification/Education Requirements for Entry Positions</a> </li> 
#     </ol></li>
# <li><a href="#concl">Conclusion</a></li>
# <ol>
#     </p>

# # A Brief Anecdote <a name="intro"> </a> 
# 
# I still remember the first time a tone-deaf recruiter for a prominent tech company aggressively pitched to me the "diversity hire" program for their company. As a gay asian who still hadn't fully grasped how tilted the industry was, I cringed as a white woman repeatedly equated "junior level positions" as "amazing opportunities for minorities and women" while a panel of senior, white, male engineers sat behind her waiting to chime in. The only women present were all juniors/interns in decidedly nontechnical roles which only served to further damage the optics of the situation.
# 
# Let me clarify: I don't believe that the institution or these people were racist. They definitely seemed quite sincere in their desire to attract more individuals of color and sexuality. But the situation forever left a sour taste in my mouth. Since then, I've always associate the company with implicitly assuming that minorities inherently belonged in junior positions. That I was a number to fill a quota that would sell more units. And that, **even if hired, I would have to constantly justify my presence as someone capable and not simply a "minority unicorn" hire.**
# 
# Put simply, if they weren't as prestigious as they were, I would never apply to them. **Given other equal options, I would likely turn them down.**
# 
# This competition topic, as a result, means quite a lot to me as I believe that a lot of racial/gender/sexuality bias begins by these subtle interactions, the phrasing, before individuals even have their resumes submitted to HR. **Because it is insufficient for an employer to declare that they are an accepting and diverse environment; their language and the design of their materials need to reflect that desire as well. ** And I am of the firm belief that the changes recommended here won't simply improve the diversity of the applicant pool but are simple and actionable changes that will improve the candidate pool as a whole. 
# 
# So, without further ado, let's discuss phrasing and how the City of LA's job postings can be improved.
# 
# **Disclaimer for nontechnical readers like Recruiters, Policy Makers, etc:** I would suggest skipping to the <a href="#demog">Job Demographics: Salaries, Word Counts, and More</a> section from here as that is where the bulk of the analysis lies. For the Data Preparation section, I will assume you are familiar with things such as Big O notation as well as common libraries and database schemas like SQL, scikitlearn, and others.

# <a name="prepa"> </a>
# # Data Preparation 
# 
# A brief rundown of the technologies used and their properties: 
# * Python was the language used in order to cleanse the data into the required .csv format
#     * The majority of libraries listed below are either native to Python or popular open-source libraries that extend Python's functionality.
# * Pandas was both used for storing/converting the data into .csv and providing a convenient framework to analyze and visualize the data later
# * Numpy is included as a mandatory requirement for Pandas as it provides optimized computation for multi-dimensional arrays and matrixes
# * re is Python's native regular expression matching library which allows us to search for generalized patterns in the text
# 
# Critically, if you're following along with the code, it's important to understand re as it greatly simplifies pattern recognition searching within strings. This allows us to abstract away a lot of otherwise lengthy code and is generally just useful when working with a lot of text-based data. Here's [a useful primer from w3schools](https://www.w3schools.com/python/python_regex.asp) in case you're unfamiliar and would like some reference material.

# In[ ]:


# Importing all the required libraries mentioned above and also establishing the file paths we'll be checking for files from
import re
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from itertools import islice
import os

# Notably, if you want to automate this script, simply point it to some directory where new job postings are aggregated
# You can then perform this operation as a batch job and process the collected data from there
bulletin_dir = '../input/data-science-for-good-city-of-los-angeles/cityofla/CityofLA/Job Bulletins'
additional_data_dir = '../input/data-science-for-good-city-of-los-angeles/cityofla/CityofLA/Additional data/'

# countWords should be defined as a function of the data-cleaner class for readability
def countWords(string):
    word_count = 0
    string = re.sub("\d+", " ", string)
    for char in '-.,\n':
        string=string.replace(char,' ')
    wordsList = string.split()
    word_count += len(wordsList)
    return word_count

data_dictionary = pd.read_csv(additional_data_dir + 'kaggle_data_dictionary.csv', header=None)
data_dictionary.at[11, 0] = "EXPERIENCE_TYPE"
data_dictionary = data_dictionary.drop([20, 21], axis=0)
data_dictionary = data_dictionary.drop([18], axis=0)
data_dictionary.head(25)


# <a name="metho"> </a>
# ## Methodology And Runtime Analysis 
# 
# At a high level, the below script is pointed towards a specific directory and steps through the lines of each .txt file within that directory, searching for specific strings that mark a particular segment (e.g. "ANNUAL SALARY"). From there, it steps through a specific series of logical steps to properly capture the data contained within that particular subsection according to the specifications set forth by the competition's rules. To maintain readability within the core loop, these logical steps are contained within the DataCleaner helper class.
# 
# One of the key benefits of the below implementation is that by performing a singular pass through each document, **it can scale efficiently as documents are added to the repository.** Specifically, the runtime is O(lf) where l is the number of lines in a document while f is the number of documents to be scanned. It will likely end up running a bit slower than that in practice due to the heavy amount of string manipulation we'll be using (individual lines might have to be scanned over several times to check for patterns) but it's nice to know that it's about as fast as we can reasonably get it.
# 
# One important drawback, however, is that **pattern searching is extremely brittle and will cease to work if the formatting of the document deviates too strongly from the previously established template.** While we can work around this by trying to make the patterns we search for as generalized as possible to account for human error, it might be ideal to train a simple classification AI later by using the data collected from this script that can automatically detect if text belongs to a specific category and process it from there rather than attempting to predict every conceivable possible way for a human to break the template. In the interim, however, this process is effective for the task at hand.

# In[ ]:


# Loading and prepping the data of private sector jobs obtained from the Online Job Postings dataset
privateSectorJobs = pd.read_csv('../input/jobposts/data job posts.csv')
privateSectorJobs['WORD_COUNT'] = privateSectorJobs['jobpost'].apply(countWords)

# Loading a list of gender-biased words based on the following paper: 
# http://gender-decoder.katmatfield.com/static/documents/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf
maleBiasWords = {'active', 'adventurous', 'aggressive', 'ambitious', 'analyze'
                'assertive', 'athletic', 'autonomous', 'battle', 'boast', 'challenge',
                'champion', 'competitive', 'confident', 'courageous', 'decision', 'decisive',
                'defend', 'determined', 'dominant', 'driven', 'fearless', 'fight', 'greedy'
                'head-strong', 'headstrong', 'hierarchical', 'hierarchy', 'hostile', 'impulsive',
                'independent', 'independence', 'individual', 'intellect', 'lead', 'logic',
                'objective', 'opinion', 'outspoken', 'persist', 'principle', 'reckless', 'self-confident',
                'self', 'stubborn', 'superior', 'unreasonable'}
femaleBiasWords = {'agree', 'affectionate', 'child', 'cheerful', 'collaborate', 'commit', 'communal'
                   'compassionate', 'connect', 'considerate', 'cooperative', 'dependent', 
                   'emotional', 'empathetic', 'feel', 'flatterable', 'gentle', 'honest', 'inclusive',
                   'interpersonal', 'interdependent', 'interpersonal', 'kind', 'kinship', 'loyal'
                   'modest', 'nag', 'nurturing', 'pleasant', 'polite', 'quiet', 'responsive', 'submissive', 
                   'supportive', 'sympathetic', 'sharing', 'tender', 'together', 'trustworthy', 'understanding',
                   'warm', 'yield', }

numberWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen"]

# Creating a HashMap (Dictionary) for counting which gender-biased words occur most frequently
maleBiasCount = {}
for word in maleBiasWords:
    maleBiasCount[word] = 0
femaleBiasCount = {}
for word in femaleBiasWords:
    femaleBiasCount[word] = 0
numberDict = {}
# Create a HashMap for converting numbered words later on
for idx, num in enumerate(numberWords):
    numberDict[num] = (idx+1)

# Compendium of all the helper methods for the main data-mining loop
class DataCleaner:
    # Returns index where next nonempty line begins
    # Ensure to initialize to currentIndex+1 to index if trying to move from a line with text on it
    def skipWhiteLines(index, fileLines):
        index+=1
        line = fileLines[index].strip()
        while(len(line)==0):
            line = fileLines[index+1].strip()
            index+=1
        return index

    # Updates index value and skips (tempIndex-index) iterations of loop
    def skipIterations(tempIndex, index):
        n = tempIndex - index
        next(islice(it, n, n), None)
        return tempIndex

    # Detects whether salary is in range or flat-rate format and outputs cleaned string
    def salaryFormatDetect(line):
        line = line.lower()
        salariesRange = re.search("\$*\d+,\d+ *t", line)
        salariesFlat = re.search("\$*\d+,\d+;*\.*\(*", line)
        if(salariesRange):
            salaries = re.sub(" to ", "-", salariesRange.string)
            salaries = re.sub("\$ +", "$", salaries)
            salaries = re.findall("\$\d+,*\d+-\$,*\d+,*\d+", salaries)[0]
            salaries = salaries.split(';')[0]
            salaries = salaries.split('.')[0]
        elif(salariesFlat):
            salaries = salariesFlat.string.split(" ")[0]
            salaries = re.sub("\$ +", "$", salaries)
            salaries = re.split(" *\(", salaries)[0] + " (flat-rated)"
            salaries = salaries.split(';')[0]
            salaries = salaries.split('.')[0]
            if(" (flat-rated)" not in salaries):
                salaries = salaries + " (flat-rated)"
        else:
            salaries = "$62,118"
        salaries = re.sub(",", "", salaries)
        return salaries
    
    def dwpSalaryDetect(line):
        salariesDWP = re.search("Department of Water and Power is \$\d+", line) 
        if(salariesDWP):
            salaryDWP = re.split("is *", salariesDWP.string)[1]
            entry_salary_dwp = dc.salaryFormatDetect(salaryDWP)
        else:
            entry_salary_dwp = None  
        return entry_salary_dwp
    
    def openDateCleaner(line):
        job_bulletin_date = line.split("Open Date:")[1].split("(")[0].strip()
        # Clean dates that lack a starting 0 e.g. 4-13-18 -> 04-13-18
        if(len(job_bulletin_date) < 8):
            job_bulletin_date = '0' + job_bulletin_date
        # Other dates have YYYY which should be cleaned to YY e.g. 4-13-2018 -> 4-13-18
        elif(len(job_bulletin_date) > 8):
            job_bulletin_date = job_bulletin_date[:6] + job_bulletin_date[8:]
        return job_bulletin_date
    
    # Checks both line where EXAM begins and next line for exam typing
    def examTypeDetect(line1, line2):
        op = (re.search("OPEN", line1) or re.search("OPEN", line2))
        inter = (re.search("INTER", line) or re.search("INTER", line2))
        depar = (re.search(" DEPARTMENTAL", line) or re.search(" DEPARTMENTAL", line2))
        if(op and inter):
            exam = "OPEN_INTER_PROM"
        elif(op):
            exam = "OPEN"
        elif(inter):
            exam = "INT_DEPT_PROM"
        elif(depar):
            exam = "DEPT_PROM"
        else:
            exam = "Not Found"
        return exam
    
    # Takes in requirements block of job postings and returns a list containing all the possibly null values in a job posting e.g. education_major
    # All helper functions for parseRequirements are below its code block
    def parseRequirements(reqList, reqData):
        reqLines = iter(enumerate(reqList))
        reqNumber = 1
        education_type, education_length, education_major, experience_type, = None, None, None, None
        experience_length, course_count, course_length, course_subject = None, None, None, None
        experience_title, experience_alt_title, experience_job_function = None, None, None
        
        for i, line in reqLines:
            requirement_set_id = reqNumber
            requirement_subset_id = 'a'
            
            education_type = dc.educationTypeDetect(line)
            if(education_type):
                education_length = dc.educationLengthDetect(line)
                if(education_type == 'COLLEGE OR UNIVERSITY'):
                    education_major = dc.educationMajorDetect(line)
            else:
                education_length = None
                education_major = None
                
            experience_type = dc.experienceTypeDetect(line)
            if(experience_type):
                # Length tends to come before experience while actual titles come afterwards
                # RegEx also gets tricky with titles that are more than 2 words long. Can create a Set for all job titles and search the string for each
                # But that can possibly end up being more inefficient in both space/time complexity.
                length = re.split("experience", line)[0]
                if(len(re.split("experience", line)) > 1):
                    title = re.split("experience", line)[1]
                else:
                    title = length
                if(re.search("college|school|apprenticeship", length)):
                    length=re.split("college|school|apprenticeship", length)[1]
                experience_length = dc.experienceLengthDetect(length)
                experience_job_function = length
                titles = re.findall("[A-Z][a-z]+ [[A-Z][a-z]+]*", title)
                if(len(titles) > 1):
                    experience_title = titles[0]
                    experience_alt_title = titles[1]
                elif(titles):
                    experience_title = titles[0]
                else:
                    experience_title = None
            else:
                experience_length = None
                experience_title = None
                if(education_type):
                    experience_job_function = None
                else:
                    experience_job_function = line
            
            course_count = dc.courseCountDetect(line)
            if(course_count):
                course_subject = dc.educationMajorDetect(line)
            else:
                course_subject = None
            if(re.search("semester|quarter", line)):
                course_length = dc.courseLengthDetect(line)
            else:
                course_length = None
                
            # Check for requirement subset
            firstElement = line.split(" ")[0].strip()
            if(re.search("\(*[a-z]\)|\(*[A-Z]\)|[a-z]\.|[A-Z]\.", firstElement)):
                reqNumber = reqNumber - 1
                requirement_set_id = reqNumber
                firstElement = firstElement.split("\t")[0].lower()
                firstElement = re.sub('[^a-zA-Z]+', '', firstElement)
                # Concatenate first info on subset with set
                if(firstElement == 'a'):
                    reqNumber += 1
                    reqData[len(reqData)-1][7] = experience_job_function
                    reqData[len(reqData)-1][8] = course_count
                    reqData[len(reqData)-1][9] = course_length
                    reqData[len(reqData)-1][10] = course_subject
                    continue
                requirement_subset_id = firstElement
                
                #Pull the appropriate data from the previous entry when a subset
                education_type = reqData[len(reqData)-1][4]
                education_length = reqData[len(reqData)-1][3]
            
            reqNumber += 1
            reqData.append([job_class_title, requirement_set_id, requirement_subset_id, education_length, education_type, education_major,
                           experience_length, experience_type, experience_title, experience_alt_title, experience_job_function, course_count, course_length, course_subject])
            
        return reqData
    
    def educationTypeDetect(line):
        if(re.search("college|university", line)):
            education_type = "COLLEGE OR UNIVERSITY"
        elif(re.search("school", line)):
            education_type = "HIGH SCHOOL"
        elif(re.search("apprenticeship", line)):
            education_type = "APPRENTICESHIP"
        else:
            education_type = None     
        return education_type
    
    def experienceTypeDetect(line):
        if(re.search("full-time", line)):
            exp_type = "FULL_TIME"
        elif(re.search("part-time", line)):
            exp_type = "PART_TIME"
        else:
            exp_type = None     
        return exp_type
    
    def educationMajorDetect(line):
        education_major = ""
        majors = re.findall("[A-Z][a-z]+ *[a-zA-Z]*,", line)
        for m in majors:
            m = re.sub(",", "", m)
            education_major = education_major + m.upper()
            if(len(majors) > 1):
                education_major = education_major + "|"
        if(education_major == ""):
            education_major = None
        return education_major
    
    # Currently operates under the presumption that # of years/months comes before type e.g. 4 years of college vs attended college for 4 years
    # This is due to ambiguity when both education and experience length are within the same line e.g. 4 years of college and 2 years of related work 
    # (How does one determine with regular expressions which belongs to which? Closest proximity would not work, etc. What about handling other cases?)
    # Ultimately requires more advanced NLP knowledge that I do not have currently.
    def educationLengthDetect(line):
        line = re.split("college|school|apprenticeship", line)[0]
        line = dc.numberConversion(line)
        education_length = dc.lengthCalculator(line)
        # A master's degree is typically 6 years of combined schooling, hence the 6
        if(re.search("[mM]aster", line)):
            education_length = 6
        # Similarly, while most PhD's take longer than 8 years, 8 is a fairly reasonable number to place as required schooling
        if(re.search("[dD]octorate|PhD", line)):
            education_length = 8
        if(education_length == 0):
            education_length = None
        return education_length
    
    def experienceLengthDetect(line):
        line = dc.numberConversion(line)
        exp_length = dc.lengthCalculator(line)
        if(exp_length == 0):
            exp_length = None
        return exp_length    
    
    def courseCountDetect(line):
        count = None
        line = dc.numberConversion(line)
        countMatch = re.search("\d+ course", line)
        if(countMatch):
            countMatch = re.sub(" course", "", countMatch.group())
            count = int(countMatch)
        return count
    
    def courseLengthDetect(line):
        line = dc.numberConversion(line)
        totalLength = ""
        semesterMatch = re.search("\d+ semester", line)
        quarterMatch = re.search("\d+ quarter|\d+ units", line)
        if(semesterMatch):
            semesterMatch = re.sub(" semester", "", semesterMatch.group())
            totalLength = totalLength + semesterMatch + "M"
        if(quarterMatch):
            quarterMatch = re.sub(" quarter", "", quarterMatch.group())
            quarterMatch = re.sub(" units", "", quarterMatch)
            totalLength = totalLength + "|" +quarterMatch + "Q"
        if(totalLength == ""):
            totalLength = None
        return totalLength
    
     # Converts written versions of numbers to integers for easier retrieval (e.g. two -> 2)
    def numberConversion(line):
        line = re.sub("-", " ", line)
        for word in line.split():
            if(word.lower() in numberDict):
                line = re.sub(word, str(numberDict[word.lower()]), line)
        return line
    
    def lengthCalculator(line):
        totalLength = 0
        yearMatch = re.search("\d year", line)
        monthMatch = re.search("\d month", line)
        if(yearMatch):
            yearMatch = re.sub(" year", "", yearMatch.group())
            totalLength += int(yearMatch)
        if(monthMatch):
            monthMatch = re.sub(" month", "", monthMatch.group())
            totalLength += (0.1 * int(monthMatch))
        return totalLength
        


# In[ ]:


dc = DataCleaner
data = []
reqData = []
diversityData = []

# Main Data-Mining Loop
for filename in os.listdir(bulletin_dir):
    with open(bulletin_dir + "/" + filename, 'r', errors='ignore') as file:
        lines = file.readlines()
        it = iter(enumerate(lines))
        job_class_title, job_duties, requirements, license_required = "", "", "", None
        
        for index, line in it:
            # Since job titles are always the first *written* line (some docs have leading white space), we can apply this condition
            if(len(job_class_title) < 2):
                job_class_title = line.split("Class")[0].strip().upper()
            if "Open Date:" in line:
                job_bulletin_date = dc.openDateCleaner(line)                 
            if "Class Code:" in line:
                job_class_no = line.split("Class Code:")[1].strip()[:4]      
                
            if "ANNUAL SALARY" in line:
                tempIndex = dc.skipWhiteLines(index, lines)
                line = lines[tempIndex].strip()               
                # Check for the three types of salary formats in the next non-empty line after ANNUAL SALARY
                entry_salary_gen = dc.salaryFormatDetect(line)
                entry_salary_dwp = dc.dwpSalaryDetect(line)
                # Check if the position is only offered within the DWP and should therefore be put as _gen
                if(entry_salary_dwp and line.strip()[0] == 'T'):
                    salaryDWP = re.split("is *", line)[1]
                    entry_salary_gen = dc.salaryFormatDetect(salaryDWP)
                # If DWP salary specification was not in same line as general salary, check if it exists below
                tempIndex = dc.skipWhiteLines(tempIndex, lines)
                line = lines[tempIndex].strip()
                entry_salary_dwp = dc.dwpSalaryDetect(line)
                index = dc.skipIterations(tempIndex, index)
                
            if "DUTIES" in line:
                tempIndex = dc.skipWhiteLines(index, lines)
                line = lines[tempIndex].strip()
                job_duties = line
                while(re.search("[A-Z]{4}", line) is None):
                    tempIndex = dc.skipWhiteLines(tempIndex, lines)
                    line = lines[tempIndex].strip()
                    job_duties = job_duties + line
                index = dc.skipIterations(tempIndex, index)
            
            # Requirements are taken in bulk to be processed later to ensure appropriate number of entries due to how data is listed in the graph
            if re.search("REQUIREMENT", line):
                tempIndex = dc.skipWhiteLines(index, lines)
                line = lines[tempIndex]
                requirement = ""
                while(re.search("[A-Z]{3}", line) is None):
                    requirement = requirement + line
                    tempIndex = dc.skipWhiteLines(tempIndex, lines)
                    line = lines[tempIndex]
                index = dc.skipIterations(tempIndex, index) 
                
            if re.search("EXAMINATION", line):
                exam = dc.examTypeDetect(line, lines[dc.skipWhiteLines(index, lines)])
                
            if re.search("may require a valid California driver's license", line):
                license_required = "P"
            elif re.search("license is required", line):
                license_required = "R"
        
        # Currently implemented by parsing the entire document again separately. Should be more neatly implemented within said loop. 
        # O(lf) still holds but is not optimized. 
        word_count = 0
        male_bias = 0
        female_bias = 0
        for line in lines:
            word_count+= countWords(line)
            line = line.split()
            for word in line:
                if(word in maleBiasWords):
                    male_bias += 1
                    maleBiasCount[word] = maleBiasCount[word] + 1
                elif(word in femaleBiasWords):
                    female_bias += 1
                    femaleBiasCount[word] = femaleBiasCount[word] + 1
        
        # Parse collected requirement block separately as certain blocks of information e.g. exam_type come after requirements in a document
        requirementsList = requirement.splitlines()
        reqData = dc.parseRequirements(requirementsList, reqData)
    
        data.append([filename, job_bulletin_date, job_class_title, job_duties, job_class_no, exam, 
                     entry_salary_gen, entry_salary_dwp, license_required])
        diversityData.append([job_class_title, word_count, male_bias, female_bias])

reqDF = pd.DataFrame(reqData) 
reqDF.columns = ["JOB_CLASS_TITLE", "REQUIREMENT_SET_ID", "REQUIREMENT_SUBSET_ID", "EDUCATION_LENGTH", "EDUCATION_TYPE", "EDUCATION_MAJOR",
                "EXPERIENCE_LENGTH", "EXPERIENCE_TYPE", "EXP_JOB_CLASS_TITLE", "EXP_JOB_CLASS_ALT_RESP", "EXP_JOB_CLASS_FUNCTION", "COURSE_COUNT", "COURSE_LENGTH", "COURSE_SUBJECT"]
df = pd.DataFrame(data)
df.columns = ["FILE_NAME", "OPEN_DATE", "JOB_CLASS_TITLE", "JOB_DUTIES", 
              "JOB_CLASS_NO","EXAM_TYPE", 'ENTRY_SALARY_GEN', 'ENTRY_SALARY_DWP', "DRIVERS_LICENSE_REQ"]

# Separate DF used for later analysis
diversityDF = pd.DataFrame(diversityData)
diversityDF.columns = ["JOB_CLASS_TITLE", "WORD_COUNT", "MALE_BIASED_WORDS", "FEMALE_BIASED_WORDS"]

# Join DF's based on job title to ensure jobs with multiple requirements have their entries grouped together and then order based on data dictionary
combinedDF = df.join(reqDF.set_index('JOB_CLASS_TITLE'), on='JOB_CLASS_TITLE')
colShift = ["FILE_NAME", "OPEN_DATE", "JOB_CLASS_TITLE", "JOB_DUTIES", "JOB_CLASS_NO", "REQUIREMENT_SET_ID", "REQUIREMENT_SUBSET_ID",
            "EDUCATION_LENGTH", "EDUCATION_TYPE", "EDUCATION_MAJOR","EXPERIENCE_LENGTH", "EXPERIENCE_TYPE", "EXP_JOB_CLASS_TITLE", "EXP_JOB_CLASS_ALT_RESP", 
            "EXP_JOB_CLASS_FUNCTION", "COURSE_COUNT", "COURSE_LENGTH","COURSE_SUBJECT", "DRIVERS_LICENSE_REQ", "EXAM_TYPE", 'ENTRY_SALARY_GEN', 'ENTRY_SALARY_DWP']
combinedDF = combinedDF[colShift]
combinedDF.head(10)

# Replace with preferred path for output
#combinedDF.to_csv('job_data.csv')


# <a name="evalu"> </a>
# ## Evaluation and Areas of Improvement 
# 
# To evaluate the cleanliness of the data after extraction, a number of different methods were utilized such as:
# 
# * Checking the unique values/range of each column using .unique() to make sure they match the intended format/content
# * Examination of various edge cases uncovered while performing initial extraction and then continuously running against them (e.g. spacing typos)
# * Manual inspection against specific, randomly chosen entries to ensure the appropriate data was captured
# 
# In retrospect, while these methods helped account for a lot of varying types of data, it was much more time consuming than if I had generated a few tests/edge-cases of my own to evaluate my algorithm against. 
# 
# There are also several areas of improvement, critically:
# 
# * Readability can be dramatically improved by **more strictly adhering to placing all of the regex/extraction functions within the data cleaner helper class** to leave the core loop as abstracted as possible
# * Furthermore, several distinct **search patterns could be abstracted to apply more generally across different data types** instead of creating specific search patterns for similar data
# * Columns such as EXP_JOB_CLASS_FUNCTION and EXP_JOB_CLASS_TITLE also **still contain some dirty data due to how the regex searching was handled on a line by line basis as opposed to analyzing the entire document in context**
# 
# A few theorized way of tackling these issues (with tradeoffs) include:
# 
# * **Storing all city job titles in a hashset** so that one can successfully compare/extract the full job title when attempting to search for EXP_JOB_CLASS and EXP_JOB_CLASS_ALT_RESP
#     * While it is relatively low operationally (checking against a set is a O(1) operation), it effectively requires the space of O(f) where f is the number of files. The availability of space and the effectiveness of JOB_CLASS_TITLE extraction therefore determines the effectiveness of this.
# * ** Process the entire document in context via a trained ML model** as opposed to raw regex-based pattern searching. This allows more successful extraction of the data even when specific formatting is not followed and is therefore more durable.
#     * While useful for data that tends to be more abstractly laid out (e.g. job function), it might be overkill for something like salary. Furthermore, obtaining the training data necessary for such a classification engine would require strong regex capabilities/manually inputted data anyway.
#     
# With the above notes in mind, though, here is what my engine was able to extract for the Systems Analyst example. As mentioned above, things like regex searching line by line hurt my overall result but it was still able to fill in most fields successfully.

# In[ ]:


combinedDF[combinedDF['JOB_CLASS_TITLE'] == 'SYSTEMS ANALYST']


# <a name="store"> </a>
# ## Data Storage Recommendations 
# 
# Implementing this as some form of SQL-based database seems relatively straightforward due to the fairly reliable structure of the data. Due to their relationship, it would be prudent to separate fields such as "JOB_CLASS_TITLE", "ENTRY_SALARY_GEN", that only have one distinct value per file into a "Job" table which has a one-to-many relationship with a "Requirements" table with fields like "EDUCATION" which can vary based on the requirement. 
# 
# However, to facilitate faster querying in regards to notifying an employee if they are eligible for a promotion/indicating what else is necessary, it might be a good idea to add an additional field for "JOB_CATEGORY" that can encapsulate both predetermined groups such as the ones included in the City Job Paths trees as well as groups that contain similar job functions but do not belong in the same tree (e.g. Sheet Metal Worker and Heavy Duty Truck Operator might both fall under "Construction" despite not being directly related in promotion path). This can be accomplished/automated by training a classification AI that can help to automatically determine which distinct job clusters exist and which jobs fall underneath them.
# 
# In this way, instead of checking over all jobs, **an automated batch-job can be performed that only checks related jobs and offers possible suggestions for cross-department promotion provided the candidate obtains a few extra certifications or job experience** alongside the more traditional promotion path within their own department.

# <a name="demog"> </a> 
# # Job Demographics: Salaries, Word Count, and Gendered Language
# 
# Before we dive into actionable items, it's a good idea for us to get a sense of what the city's job postings are like, particularly compared to job postings outside of the government. This will allow us to have a solid understanding of not only what the city of LA has to compete against to hire more diverse talent but also highlight potential unique attributes the city can provide that for-profit entities cannot. 
# 
# To begin, let's start with the most relatively available, visible, and positive data:
# 
# <a name="salar"> </a>
# ## Salaries: Surprisingly Competitive 

# In[ ]:


def salaryToInt(salary):
    salary = re.findall("\$\d+", salary)[0]
    salary = re.sub("\$", "", salary)
    return int(salary)

def dwpSalaryDiff(gen, dwp):
    gen = re.findall("\$\d+", gen)[0]
    gen = re.sub("\$", "", gen)
    gen = int(gen)
    dwp = re.findall("\$\d+", dwp)[0]
    dwp = re.sub("\$", "", dwp)
    dwp = int(dwp)
    return (dwp-gen)

plt.figure(figsize= (9, 4))
plt.subplot(1, 2, 1)
s = df[['ENTRY_SALARY_GEN']].copy()
s.loc[:,'ENTRY_SALARY_GEN'] = s['ENTRY_SALARY_GEN'].apply(salaryToInt)
citySal = sns.distplot(s['ENTRY_SALARY_GEN'], kde=False)
citySal.set(xlabel='Base Salaries ($)', ylabel='Number of Jobs')
citySal.set_title("City Salary Distribution")

plt.subplot(1, 2, 2)
diff = df[['ENTRY_SALARY_GEN', 'ENTRY_SALARY_DWP']].copy().dropna()
diff['Difference'] = diff.apply(lambda row: dwpSalaryDiff(row['ENTRY_SALARY_GEN'], row['ENTRY_SALARY_DWP']), axis=1)
diff = sns.distplot(diff['Difference'], kde=False, color='m')
diff.set(xlabel='Difference in Salary ($)')
diff.set_title("DWP Salary Differential")


# One asset that really helps the city is that, on average, their **salaries are really competitive with the private sector**. The median base (or in same cases, flat) salary is \$79,244, well above [the average salary of Los Angeles according to Payscale](https://www.payscale.com/research/US/Location=Los-Angeles-CA/Salary) at \$62,984. Anecdotal evidence supports this as comparing the reported salaries of positions such as Financial Analyst (\$51-81k with 64k average vs the city offering \$68k as a base) show that there's no significant difference.
# 
# Granted, **this inference relies off the reported salaries on sites such as payscale and glassdoor being accurate which is indiscernable**. Taken as truth, however, this means that improving the odds of hiring diverse talent won't necessarily require massive investment in terms of attempting to raise salaries to become more competitive with the private sector. What could use improvement is more how these salaries are conveyed to potential applicants, which will be discussed later.
# 
# An interesting quirk to mention before moving on is that the DWP median salary, in aggregate, is around the same as the general salary (\$78905). However, it's important to note that the average pay difference for an identical position with the DWP is an increase of around \$13k (\$13285) but **it is usually unclear what additional requirements are necessary for employment with the DWP as opposed to the generic pool**.
# 
# Lastly, it is important to mention that the only position that does not have a salary explicitly listed is Airport Police Specialist as it is "Salary scale pending. Salary to be determined prior to appointment." The data for that has been substituted with the Airport Police salary of \$62,118 since not only is that a close match in terms of job function but also because it is relatively close to the medium salary
# 
# Now, let's transition to more troublesome data.
# 
# <a name="count"> </a>
# ## Word Counts: Needlessly Verbose 
# 

# In[ ]:


plt.figure(figsize= (9, 4))
plt.subplot(1, 2, 1)
cityLength = sns.distplot(diversityDF['WORD_COUNT'], kde=False)
cityLength.set(xlabel='Number of Words', ylabel='Number of Jobs')
cityLength.set_title("City Post Length")
#df['WORD_COUNT'].median()

plt.subplot(1, 2, 2)
privateLength = sns.distplot(privateSectorJobs['WORD_COUNT'], kde=False, color='r')
privateLength.set(xlabel='Number of Words')
privateLength.set_title("Private Sector Post Length")
#privateSectorJobs['WORD_COUNT'].mean()
diversityDF['WORD_COUNT'].mean()


# One of the first things that I noticed while initially viewing the job postings was how verbose many of the job postings were compared to similar job postings in the private sector. To determine whether this gut feeling was true, I decided to compare the number of words within city job postings to [a dataset of Armenian private sector jobs](https://www.kaggle.com/madhab/jobposts) and the resulting graphs showcase the dramatic difference in length.
# 
# Specifically, **the average city job posting is almost four times longer than a private sector job posting** at a whopping 1343 words compared to 361 words in the latter.
# 
# This is a critical area to improve as **text that is overly long can be prohibitively intimidating for immigrants and non-native English speakers**. Considering that many different sources state that the [average native English speaker's reading speed to be 200 words per minute](https://www.irisreading.com/what-is-the-average-reading-speed/), it follows that:
# * At 75% of a native English speaker's speed (150 words per minute), **it'll take an additional 2 minutes to read the entire average city job posting**
# * At half the speed (100 words per minute), **a non-native English speaker would need 13 minutes to read an average city post**
# * Postings with more advanced vocabulary worsen this issue, making it impractical for non-native English speakers to determine if they're eligible **even if they have perfectly functional English-speaking abilities**
# 
# This last point is important. We're not necessarily talking about people who are incapable of reading/speaking English; my mother ten years ago, for example, passed the TOEFL exam to come to work/study in America as a nurse. However, having had to proofread her letters/papers as a child, I highly doubt she would bother to even look through such a lengthy job posting despite being perfectly capable of communicating with coworkers in person. 
# 
# This is further under the assumption that writing/reading is a critical component of the job. **Many physical labor jobs, such as ones in construction, won't actually require comprehensive English proficiency** as many private-sector construction companies who ~~exploit~~ hire immigrants without documentation will attest.
# 
# Even disregarding the goal for improved diversity, **pruning these postings will improve their readability for everyone which will attract more talent overall.** It also offers the opportunity to cut down on excessive and outdated requirements/certification demands that might not accurately reflect what the job requires. 
# 
# We'll discuss some key areas where this pruning can occur after we examine one of the most popular focuses of recent diversification efforts.
# 
# <a name="gende"> </a>
# ## Gendered Language: Prevalence and Distribution 

# In[ ]:


fig = plt.figure(figsize= (9, 8))
plt.subplot(2, 2, 1)
mbw = sns.distplot(diversityDF['MALE_BIASED_WORDS'], bins=8, kde=False)
mbw.set(xlabel='Word Count', ylabel='Frequency')
mbw.set_title("# of Male-Biased Words per Posting")

plt.subplot(2, 2, 2)
commonMaleWords = pd.DataFrame.from_dict(maleBiasCount, orient='index', columns=['Count'])
commonMaleWords = commonMaleWords[(commonMaleWords.T != 0).any()]
commonMaleWords = commonMaleWords.sort_values(by=['Count'], ascending=False)
cmw = sns.barplot(data=commonMaleWords.reset_index(), y='Count', x='index')
cmw.set(xlabel='Male-Biased Words')
cmw.set_title('Frequency of Specific Male-Biased Words')
plt.xticks(rotation=90)

plt.subplot(2, 2, 3)
mbw = sns.distplot(diversityDF['FEMALE_BIASED_WORDS'], kde=False)
mbw.set(xlabel='Word Count', ylabel='Frequency')
mbw.set_title("# of Female-Biased Words per Posting")

plt.subplot(2, 2, 4)
commonFemaleWords = pd.DataFrame.from_dict(femaleBiasCount, orient='index', columns=['Count'])
commonFemaleWords = commonFemaleWords[(commonFemaleWords.T != 0).any()]
commonFemaleWords = commonFemaleWords.sort_values(by=['Count'], ascending=False)
cfw = cmw = sns.barplot(data=commonFemaleWords.reset_index(), y='Count', x='index')
cmw.set(xlabel='Female-Biased Words')
cmw.set_title('Frequency of Specific Female-Biased Words')
plt.xticks(rotation=90)

fig.tight_layout()


# For the uninitiated, gendered language are instances where **certain phrases or words ascribe a masculine or feminine connotation to the sentence** [which may subtly bias the job description towards one gender or the other](http://gap.hks.harvard.edu/evidence-gendered-wording-job-advertisements-exists-and-sustains-gender-inequality). Examples of this include using words such as "foreman" instead of "superviser" and describing desired applicants as "competitive", "dominant", or "aggressive"
# 
# This proved to be relatively tricky to tackle due to the semi-subjective nature of what adjectives are considered "masculine" vs "feminine" and is currently a very active area of research within the field of Natural Language Processing in Computer Science. I ended up opting for a relatively blunt approach (creating a simple list of common masculine and feminine nouns [based on a research paper](# http://gender-decoder.katmatfield.com/static/documents/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf) and tallying the respective amounts of each) that won't be able to capture the more nuanced instances of gendered language but, as a result, also identifies places, if any, that would be relatively easy to fix.
# 
# Additionally, before we take a deep dive into the analysis, it should be noted that **the job postings, as a whole, are relatively free of gendered language based on my findings.** Such findings are definitely a cause for celebration and deserve accolades.
# 
# Let's start by taking a quick look at what are the most male-biased postings and seeing if we can discern some pattern:

# In[ ]:


maleBiasedJobs = diversityDF[['JOB_CLASS_TITLE', 'MALE_BIASED_WORDS']].copy()
maleBiasedJobs = maleBiasedJobs.sort_values(by=['MALE_BIASED_WORDS'], ascending=False)
maleBiasedJobs.head(10)


# Broadly speaking, these positions seem to predominantly be contained within the construction industry which is historically known to be heavily skewed towards men. However, context is imporant, and it should be noted that many of these positions such as Property Officer really **only have such high scores because of repeated mentions of "open competitive exams"** as opposed to truly gender-biased language.

# In[ ]:


maleBiasedJobs.tail(10)


# Checking the job postings with the fewest male-biased words supports this as many of these positions are similarly male-dominated and belong to similar industries (e.g. construction). **If male-biased language does exist within any of the job postings, it would likely be far more subtle than mere word-choice** as a result.

# In[ ]:


femaleBiasedJobs = diversityDF[['JOB_CLASS_TITLE', 'FEMALE_BIASED_WORDS']].copy()
femaleBiasedJobs = femaleBiasedJobs.sort_values(by=['FEMALE_BIASED_WORDS'], ascending=False)
femaleBiasedJobs.head(10)


# Analyzing the positions that display the most female-biased languages reveals similar results, with certain positions like Senior City Planner containing both male and female oriented language. This again indicates that **whatever biased word-choice that does exist is likely incidental as opposed to inadvertently creating tinted language.**
# 
# 

# <a name="forma"> </a>
# # Actionable Formatting Improvements 
# 
# Now, ideally, we would have each posting available in multiple languages with pictures of a diverse workforce pretending to happily work on something or other. However, such actions are both nontrivially expensive and won't solve underlying issues such as job postings being incomprehensible long/complicated.
# 
# So, instead, let's dive into some actionable tasks that will improve the approachability of these job postings not only for those who have English as a second language but for everyone. 
# 
# <a name="cut"> </a>
# ## Cut Word Count and Reading Level 
# 
# <a href="#count">As previously mentioned,</a> the job postings in aggregate are unreasonable bulky in comparison to their private sector counterparts which generally harms everyone but also disproportionately affects non-native English speakers. Manual inspection reveals that the bulk of these superfluous words are concentrated into a few distinct sections:
# 
# * **Process Steps:** While critical, these can usually be condensed and are really just requirements in disguise. Driver's License requirements, for example, are often nestled here when they should just be in the requirements section. These are also things that prospective candidates can simply be informed of after being screened by HR.
# * **Certification Requirements:** We'll discuss these, specifically, later but they oftentimes add an absurd amount of verbage that is both difficult to parse and generally discouraging for applicants when they see overly long lists of "requirements".
# * **Miscellaneous Notes/Forms:** Again, while critical, a lot of this information can simply be relayed by a recruiter/HR instead of front-loaded at the application page. Form collection can also be automated by having candidates simply fill out those required forms alongside the application if doing it through an online portal.
# 
# Overall, the essential elements that can tie together the various sections that can be cut is answering the question "Can this information simply be told to a candidate we're actually interested in?" and "Will the candidate likely forget this form if we don't automate the collection of it or remind them of it later?". If the answer is yes to either of those questions, cut it.
# 
# <a name="clari"> </a>
# ## Clarify Salary Expectations and Progression 
# 
# While trying to extract the salary data, I came to realize just how *dirty* the presentation of salary was within many of the job postings. They were a few, distinct patterns for which I chose a job posting that exemplified that pattern. Examples include:
# 
# * **Listing every single salary step increase:** Principal Communications Operator (\$54,100; \$55,583; \$57,107; \$58,673; \$60,281; ... \$79,052.) 
#     * While that information might be important internally, candidates are unlikely to fully process the \$1\.4k incrementation with each salary step. It would be far more succinct to use a range.
# * **Showing two salaries with no distinction for what separates the two:** Real Estate Associate (\$46,687 to \$68,298 and \$55,164 to \$80,638.)
#     * While it mentions that new hires are typically sent to the lower range, candidates might be understandably upset if they perceive themselves as having enough experience for the second range. This is particularly apparent in non-trivial gaps in salary like the above.
# * **Including both generic and DWP salary ranges:** Air Conditioning Mechanic Supervisor (\$103,841 vs the DWP's: \$127,388)
#     * As previously established, there is oftentimes a significant difference in salary between jobs at the DWP and in the generic pool but with little explanation on how one someone can apply to one versus the other.
# 
# Honorable mention goes to Boilermaker which is one of the only jobs to go down to the cent (\$96,695.25). I don't think a quarter is particularly relevant after taxes but hey.
# 
# There is one critical flaw that connects all of these various formats though: ambiguity over what an applicant can realistically expect to make given certain attributes and growth potential. The latter is of critical importance as several surveys have concluded that [minority applicants are most often attracted to jobs with socioeconomic mobility over other factors](https://www.tandfonline.com/doi/abs/10.1080/09585191003658847#.VCdy1fldVWI) and **lack of perceived mobility within public sector jobs is what tends to cause minorities to prefer private over public sector jobs.**
# 
# At this point, I think it like to take a step back and discuss how video games illustrate and showcase possible progression paths because I think that that it provides a few lessons that we can then apply to a solution. Considering that their industry is focused on being easily accessible and exploiting addictive dopamine loops, they serve as a group place to search for inspiration when it comes to the psychology of progressive systems.
# 
# Given this, let's examine an archetypal "talent tree", *image courtesy of jeff-berry from his article on tutsplus:*
# 
# ![](https://cdn.tutsplus.com/gamedev/authors/jeff-berry/Tree.jpg)
# 
# As we can see above, various skills are distinguished from each other within self-contained nodes and pre-requisites for later levels are clearly illustrated by arrows. Each tier is also distinctly separated by height with objects of roughly equal potency sharing the same height.
# 
# We can apply this lesson, albiet in a less visual format, to showcase a clear path for growth and curb expectations of salaries and, interestingly, this involves combining aspects of the previously mentioned problematic salary formats. We start by showcasing a range of salaries and then break it down into distinct levels based on pre-requisite skills. 
# 
# Concretely, here's an example of how I would make this using the Systems Analyst position:
# * **Salary ranges from \$68,611 to \$100,307, based on level**
# * **Level 1:** \$68,611 - \$75,000 (Bachelor's Degree in IT|CS|related or 2 Years of Experience as Systems Aide)
# * **Level 2:** \$80,000 - \$90,000 (Bachelor's + 1 Year of Experience or 3 Years of Experience in related role or 2 Years and applicable certification)
# * **Level 3:** \$90,000 - \$100,307 (Bachelor's + 2 Years of Experience or 4 Years of Experience in related role or 3 years and applicable certification)
# * **Promotion Options:** \[Insert applicable promotion options here\]
# 
# Not only does this more clearly delineate what are the varying levels of requirements, it also **provides multiple, concrete options for any individual to reach a new level and gives inexperienced candidates brackets to compete with each other** as opposed to having to necessarily compete against the most experienced candidate in the applicant pool. It also serves a dual function of reducing the overall length by effectively combining two previously distinct sections into one.
# 
# <a name="cleans"> </a>
# ## Cleanse Excessive Education/Experience Requirements for Entry Positions
# 
# I'd like to highlight the Systems Analyst position again because I feel like it is a prime example of this problem.
# 
# <a href="https://ibb.co/WyL860h"><img src="https://i.ibb.co/k8tbxJ7/absurd-Certs.jpg" alt="absurd-Certs" border="0"></a>
# 
# There is no way on God's green earth that **anyone** regardless of their English reading proficiency will enjoy reading something that goes on to list **46 certifications** and can comprehensibly determine which ones they have, which ones they lack, and **which ones are actually required for the job.** 
# 
# Forget about [how standardized testing, and therefore certification exams, tends to discriminate against minorities and the impoverished](http://www.centralislip.k12.ny.us/UserFiles/Servers/Server_20856499/File/Teacher%20Pages/Anthony%20Griffin/My%20Blog/standardizedtestsdiscriminateagainstminorityandlowerincomestudents.pdf). By itself, it is simply unreasonable to think that the average individual would possess more than 2-3 certifications, much less 46. 
# 
# Instead of listing every single possible certification under the sun (certifications might not be the best predictor of performance anyway), the list should be culled to the one or two that might have any significant bearing on the job at hand. Any other certifications that the candidate possesses can then be examined by HR with the list. **Candidates do not need access to the entire list of possible accepted certifications.** 
# 
# Granted, that particular position is a bit of an outlier compared to the rest of the job postings. However, there still exists a trend where **several positions that are highly discouraging for the average newcomer to the industry to apply due to a lack of certification/experience despite being "entry level positions".**
# 
# One example of this, for example, is by analyzing the progression from Customer Service Representative -> Systems Aide -> Systems Analyst. Systems Analyst essentially works as the entry level position for someone who is college educated and functions well as such. However, the same progression would **require a minimum of six years if one was starting as a Customer Service Rep (4 as a Customer Service Rep, 2 as a Systems Aide), assuming that the employee was not passed over for candidates with more direct experience/education.** This does not include the fact that Service Reps require 2 years of experience to even obtain the job according to the requirements of a "entry level" position, bringing the total number of years to 8. This includes the fact that being a Service Rep is not even included in the promotion pathing of a Systems Analyst.
# 
# Comparatively, working at a company like AT&T, a person could reasonable expect to become a store manager in 1-2 years and a regional manager in the same 5-6 years of time. And while these positions might not pay as much, the path is far more clear with training provided along the way. 
# 
# Therefore, to continue with that growth-oriented mindset, it would be highly advantageous to **mention in the job postings that candidates without x certification/experience will be trained to obtain it within 6 months**, during which time they might be placed at a lower salary level. There can additionally be a clause, like with many other private companies, that the candidate will be contractually bound to remain within the government (note, not the specific position but government positions as a whole) for 1-2 years as a return on investment.
# 
# This opens up a huge field of opportunity for impoverished applicants who might not have the time/resources to be able to study and take that certification exam prior to obtaining this government position as [1 in 20 Americans are currently working two or more jobs in order to survive](https://www.bls.gov/opub/ted/2018/4-point-9-percent-of-workers-held-more-than-one-job-at-the-same-time-in-2017.htm?view_full). It also **offers an alternative path for socioeconomic mobility than going to college which, again, is one of the biggest attractions to a position for all minority groups.**

# # Conclusion
# 
# While these are a few paths to increase diversity, one of the most effective means of attracting more diverse talent is, unfortunately, to simply have more diverse talent to begin with. However, hopefully these changes can help reduce any artificial barriers that prevent otherwise qualified candidates from applying!
