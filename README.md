# Project Template

### Repo (w/ python .gitignore template)
Create a new repository from Github and make sure you use the Python .gitignore template. Then git clone the repo on local machine.<br>
Make sure that .gitignore file has the following two entries (if not them add them manually).
```
.env
venv
```

### Visual Studio Code Workspace
Visual studio Code: File > Open Folder (select the repo root dir).<br>
File > Save Workspace As (qant.machine-learning.code-workspace).

### Dependency file
Copy/create in root a requirements.txt in which you specify the libs needed for the project.

### Startup Class
Create a "program" directory under the root directory. This will house the source code.<br>
Create a "main.py" class under program directory and add the following 2 lines of code:
```
if __name__ == "__main__":
    print("Hello ML!")
```

### Environment varibales file
In project root add a **.env** file for storing environment variables (make sure it's git ignored).<br>

### Create venv virtual environment 
From Visual Studio Code (or not), from root directory, open a terminal window (Terminal > New Terminal).<br>
Check python version in the bottom right corner. Click on it then click on "Select at workspace level"<br>
Now select **Python ver ('venv':venv)**. Make sure you use this Python to activate the virtual environments and install the requirements.

Create the virtual environment, then check venv folder was created:
```
python3 -m venv venv
```

### Activate virtual environment and install dependencies
To activate the environment you have a scripts folder and an **activate** powershell script. Just call it from the terminal:
```
venv\scripts\activate
```
*To deactivate the virtual environment just run ```deactivate```

Once the virtual environment has been activated, install the necessary libraries by running:
```
pip3 install -r requirements.txt
```

### Run the program
To test if it's working, make sure the virtual environment is activated, cd into program directory and run main.py:
```
venv\scripts\activate
cd program
python3 main.py
```
