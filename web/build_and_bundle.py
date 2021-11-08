import subprocess
import re

subprocess.run("rm package-lock.json", shell=True, check=True)
subprocess.run("npm install", shell=True, check=True)
subprocess.run("npm run build", shell=True, check=True)
subprocess.run("rm -rf ../serverless/flask-server/build", shell=True)
subprocess.run("cp -r build ../serverless/flask-server/", shell=True)
