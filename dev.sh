# Ensure virtualenv exists and create it if it does not exist
if [ ! -d "./env" ]; then
	python3 -m venv env
fi

# Activate the virtualenv and ensure it is up to date
source ./env/bin/activate
pip install -e .

# Configure the Flask environment variable so Flask knows what to run 
export FLASK_APP=SuperHeroArena

# Optional Development Flag 
export FLASK_ENV=development

# Run the Flask application
flask run
