# Create the main project directory
mkdir -p video_creator_project

# Change to the project directory
cd video_creator_project

# Create the agents directory and its files
mkdir -p agents
touch agents/__init__.py
touch agents/content_agent.py
touch agents/translation_agent.py
touch agents/speech_agent.py
touch agents/image_agent.py
touch agents/video_agent.py

# Create the utils directory and its files
mkdir -p utils
touch utils/__init__.py
touch utils/language_utils.py

# Create the main files
touch config.py
touch main.py
touch requirements.txt

# Display the created structure
tree