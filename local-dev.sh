
python -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Build HTML
make html

# View in browser
open build/html/index.html  # Mac
