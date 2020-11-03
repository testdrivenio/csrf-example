# CSRF in Flask Example

Secure Flask App

## Setup
1. Create and activate a virtual environment
1. Install the dependencies
   ```bash
    pip install requirements.txt
   ```
1. Run the Flask app
    ```bash
    python app.py
    ```
1. Serve the _index.html_ from the "hacker" folder with [http.server](https://docs.python.org/3/library/http.server.html#module-http.server)
   ```bash
   python -m http.server --directory hacker 8002
   ```