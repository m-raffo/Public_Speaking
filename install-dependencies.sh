#cd ~/Documents/Projects/PythonMH3/Public_Speaking
echo "This is a mac only script that requires brew"
brew install portaudio
cd "$(dirname "$0")"
pip3 install virtualenv
source ./venv/bin/activate
pip3 install -r ./requirements.txt 
deactivate
