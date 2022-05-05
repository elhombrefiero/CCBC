# Set names from args. Names must be lowercase.
app_name="ccbc-app"
venv_name="venv"

# Create react app.
npx create-react-app $app_name

# Material UI install.
npm install @mui/material @emotion/react @emotion/styled

# Create flask directory.
mkdir $app_name/flask

# Copy requirements and change directories.
cp requirements.txt $app_name/flask
cd $app_name/flask

# Create new app file.
touch app.py .env

# Add flask env variables.
echo "FLASK_APP=app.py" >> .env
echo "FLASK_DEV=development" >> .env

# Create a new virtual environment.
python3 -m venv $venv_name

# Activate environment.
source $venv_name/bin/activate

# Install requirements.txt.
python -m pip install -r requirements.txt

# Upgrade pip if new version is available.
pip install --upgrade pip
