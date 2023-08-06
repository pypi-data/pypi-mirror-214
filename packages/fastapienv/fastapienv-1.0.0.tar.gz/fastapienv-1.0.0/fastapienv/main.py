import os
import subprocess
from colorama import Fore, Style

def create_venv_with_fastapi(venv_name, activate_env, start_server, server_host="localhost", server_port=8000, server_reload=True):
    # Check if the virtual environment already exists
    if os.path.exists(venv_name):
        choice = input(f"The virtual environment '{venv_name}' already exists. Do you want to recreate it? (yes/no): ")
        if choice.lower() != "yes":
            print("Skipping virtual environment creation.")
            return
    
    # Create a Python virtual environment using `venv`
    subprocess.run(["python", "-m", "venv", venv_name])
    
    # Activate the virtual environment
    venv_path = os.path.join(os.getcwd(), venv_name)
    activate_script = os.path.join(venv_path, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_path, "bin", "activate")
    
    if activate_env:
        subprocess.run(activate_script, shell=True)
         # Install FastAPI within the virtual environment
        subprocess.run(["pip", "install", "fastapi", "uvicorn"])
        
        # Start the FastAPI server if specified
        if start_server:
            server_command = ["uvicorn", "main:app"]
            
            # Customize server options if provided
            if server_reload:
                server_command.append("--reload")
            if server_port:
                server_command.extend(["--port", str(server_port)])
            if server_host:
                server_command.extend(["--host", server_host])
            
            subprocess.run(server_command)

        print(f"{Fore.YELLOW} *****The virtual environment is activated. Remember to deactivate it later.*****{Style.RESET_ALL}")
        # warnings.warn("The virtual environment is activated. Remember to deactivate it later.", category=UserWarning)
        # print("The virtual environment is activated. Remember to deactivate it later.")
    
   
    
    # Deactivate the virtual environment unless specified by the user
    if not activate_env:
        subprocess.run(["deactivate"], shell=True)




def generate_fastapi_boilerplate():
    # File path for the FastAPI boilerplate code
    file_path = os.path.join(os.getcwd(), "main.py")
    
    # Check if the file already exists
    if os.path.exists(file_path):
        choice = input(f"The file {file_path} already exists. Do you want to override it? (yes/no): ")
        if choice.lower() != "yes":
            print("Skipping file generation.")
            return
    
    # Generate the FastAPI boilerplate code
    with open(file_path, "w") as file:
        file.write("""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
""")

def createFastApiEnvironment(venv_name, activate_env=False, start_server=False, server_host="localhost", server_port=8000, server_reload=True):

     # Generate FastAPI boilerplate code
    generate_fastapi_boilerplate()

    # Create the virtual environment and install FastAPI within it
    create_venv_with_fastapi(venv_name, activate_env, start_server, server_host, server_port, server_reload)

   
