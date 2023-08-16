# A simple Flask API to colorize images

## Instructions:

1. Clone the repo
    ```
    git clone https://github.com/ornob011/colorize
    ```

2. Open the directory
    ```
    cd colorize
    ```

3. Install the required libraries:

    ```
    pip install -r requirements.txt
    ```

4. Run the project:
    ```
    gunicorn -b 0.0.0.0:8000 app:app
    ```

5. Open the following link in Postman with 'post' request: 

    ```
    https://0.0.0.0:8000
    ```
6. Input an image to the file submission form in Postman.