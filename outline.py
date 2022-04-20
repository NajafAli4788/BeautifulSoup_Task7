from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, render_template

# task 7
app = Flask(__name__)
@app.route("/")
def displayJobDetails():
    
    #write a code to give call to json file and then render html page
    responseJSON = requests.get('https://raw.githubusercontent.com/AirMonkay/BeautifulSoup/main/jobDetails.json').json()

    return render_template('index.html',responseJSON = responseJSON)

# global array
jobs = []
def displayJobDetails():
    print("Display job details")

#function to get job list from url 'https://www.indeed.com/jobs?q={role}&l={location}'
def getJobList(role,location):
    url = 'https://www.indeed.com/jobs?q={role}&l={location}'
    url = url.replace("{role}",role)
    url = url.replace("{location}",location)
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")
    for job in soup.find_all('table',class_='jobCard_mainContent'):
        jobTitle = job.find('h2','jobTitle').text
        if jobTitle.startswith('new'):
            jobTitle = jobTitle.replace('new','')
        companyName = job.find('span',class_='companyName').text
        try:
            description = job.find('div',class_='job-snippet').text
        except:
            description = "None"
        try:
            salary = job.find('div',class_="salary-snippet-container").text
        except:
            salary = "None"
        jobListing = {
            'Title':jobTitle,
            'Company':companyName,
            'Description':description,
            'Salary':salary
        }
        #print(jobListing)
        jobs.append(jobListing)
    return jobs

#save data in JSON file
def saveDataInJSON(jobDetails):
    with open("jobDetails.json","w") as file:
        json.dump(jobDetails,file,indent=4)
    print("Saving data to JSON")

#main function
def main():
    # Write a code here to get job location and role from user e.g. role = input()
    print("Enter role you want to search")
    role = input()
    print("Enter location you want to search")
    location = input()
    print(role+" located in "+location)
    jobList = getJobList(role,location)
    print(jobList)
    saveDataInJSON(jobList)
    
    # Complete the missing part of this function here
    


    
if __name__ == '__main__':
    app.run(debug=True)
    main()

    