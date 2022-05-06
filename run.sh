# Ensure virtualenv exists and create it if it does not exist
if [ ! -d "./env" ]; then
	echo "Please run init.sh first"
else
	# Activate the virtualenv and ensure it is up to date
source ./env/bin/activate

# Configure the Flask environment variable so Flask knows what to run 
export FLASK_APP=SuperHeroArena

# Run the Flask application
flask run
fi
