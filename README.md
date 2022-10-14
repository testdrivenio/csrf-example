# CSRF in Flask Example

Insecure Flask App

## Setup

1. Create and activate a virtual environment

1. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

1. Run the Flask app:

    ```bash
    python app.py
    ```

1. Serve the *index.html* from the "hacker" folder with [http.server](https://docs.python.org/3/library/http.server.html#module-http.server):

    ```bash
    python -m http.server --directory hacker 8002
    ```
