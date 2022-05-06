# Ask the user for an api key
echo "Please go to https://rapidapi.com/jakash1997/api/superhero-search/ and sign up for an account.  Then subscribe to the linked api to generate an API key"
read -sp  "API Key: " APIKey

# Create/update the .env file
echo "X-RapidAPI-Key="$APIKey > .env

# Ensure virtualenv exists and create it if it does not exist
if [ ! -d "./env" ]; then
	python3 -m venv env
fi
	
# Activate the virtualenv and ensure it is up to date
source ./env/bin/activate
pip install -e .