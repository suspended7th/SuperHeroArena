# Activate the virtualenv and ensure it is up to date
source ./env/bin/activate

# Configure the Flask environment variable so Flask knows what to run 
export FLASK_APP=SuperHeroArena

# Optional Development Flag 
export FLASK_ENV=development

# Run the Flask application
flask run
