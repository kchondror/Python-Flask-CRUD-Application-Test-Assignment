# Follow the instructions below to be able to run the application locally.

## First of all, you need to have installed Python 3.11 or later (since that's the version that I used to create the app...) and Git (optional) on your machine.
After that, execute the commands below in the exact same order:

### If you are using Git, execute the commands in step 1; otherwise, go to step 2.
1. > ~ Create a new folder for the project <br> ~ Open up a terminal and use the <u>cd</u> command to navigate into the folder you just created. <br> ~ git init (to initialize a local repository) <br> ~ git pull https://github.com/kchondror/Python-Flask-CRUD-Application-Test-Assignment.git (to pull the source code from GitHub) 
2. > ~ Go to the [Project's GitHub repository](https://github.com/kchondror/Python-Flask-CRUD-Application-Test-Assignment) <br> ~ Navigate through <u>code</u> > <u>download zip</u> (to download the source code) <br> ~ Find and unzip the file <br> ~ Open up a terminal and use the <u>cd</u> command to navigate into the folder you just downloaded.

3. python -m venv env (to create a virtual environment) 
4. cd env/Scripts (go to the Scripts subfolder) 
5. activate (run the activate.bat file) 
6. cd ../../ (go back to the project's root) 
7. pip install -r requirements.txt (to install all the necessary external Python libraries for the project) 
8. pip list (<u>optional</u> to make sure that the libraries are installed successfully) 
9. "./env/Scripts/python.exe" "./apps/backend - controllers/server.py" (to finally launch the application)

### Finally, open your browser, search for: "http://127.0.0.1:5000/" and navigate through this basic web application
