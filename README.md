# Flask Image Processing API

This API allows users to upload images, processes them using a pre-trained model, and provides a URL to access the processed image.

## API Endpoints

### 1. Upload and Process Image

- **URL**: `/`
- **Method**: `POST`
- **Description**: Upload an image for processing. Returns a unique URL to retrieve the processed image.
- **Payload**:
  - `file`: The image file you want to upload.
- **Success Response**:
  - **Code**: `200`
  - **Content**:
    ```json
    {
        "message": "Image processed successfully.",
        "image_url": "/get_image/1"
    }
    ```

### 2. Retrieve Processed Image

- **URL**: `/get_image/<int:image_id>`
- **Method**: `GET`
- **Description**: Fetch the processed image using its unique ID.
- **Parameters**:
  - `image_id`: The unique ID assigned to the processed image.
- **Success Response**:
  - **Code**: `200`
  - **Content**: Processed image file.
  
- **Error Response**:
  - **Code**: `404`
  - **Content**:
    ```json
    {
        "error": "Image not found."
    }
    ```

## Setup & Execution

### Installation

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