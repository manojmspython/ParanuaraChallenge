# ParanuaraChallenge 
This application has API providing these end points:
Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}

# Requirement to run this applicaiton
Docker has been installed. This application has been dockerised so that data can be loaded and there is no hastle for environment setup.
If Docker is not already installed please follow the steps from https://docs.docker.com/get-docker/.
Once the docker is installed and verified. Lets move on the next steps.

# Environtment Setup
Run the following steps to get th application running:
  1. Naviagate to empty directory and run the below command in git bash
                  git clone https://github.com/manojmspython/ParanuaraChallenge.git
  2. run cd "ParanuaraChallenge\Paranuara"
  3. The data which will we already present in resources folder. If one wants to change these files they can changes these files. Note
     that these files are validated against schema verification. So Dont change the schema.
  4. now run :
      docker build . --no-cache  -t paranuara_backendapi && docker-compose up -d 
      
      If this step prompts for anything provide ÿes as an answer.
  5. Run "docker container ls". You can see a container with name "paranuara". That means apllication is up and running.
  6. Get the container id from previous command and run "docker exec -it <containerid> bash"
  
# Usage
** Note these api are build as GET but can very well be POST.
  
  1. Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any
     employees.
     curl -X GET http://127.0.0.1:5000/citizen/getEmployees/company=CORMORAN
     
  2. Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes      and are still alive
     curl -X GET http://127.0.0.1:5000/citizen/findFriends/name=Eugenia Thornton,Carmella Lambert
     
  3. Given 1 people, provide a list of fruits and vegetables they like
     curl -X GET http://127.0.0.1:5000/citizen/getFood/name=Eugenia Thornton
     
 # Test Usage.
    Once inside container run python manage.py test.
    
 That's it. Hope you enjoy this!
  
      
      
