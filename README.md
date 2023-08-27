# Face Recognition API

Welcome to the Face Recognition API documentation! This API allows you to compare faces using facial recognition technology. You can use this API to determine if two images contain the same person's face.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Check Server Status](#check-server-status)
  - [Compare Faces](#compare-faces)
- [Response Format](#response-format)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)
- [License](#license)

## Getting Started

To use the Face Recognition API, you need to send POST requests with base64-encoded images for comparison. Before you begin, make sure you have the required dependencies installed and the API running.

## Installation

1. Clone this repository:

   ```bash
   git clone https://git.dataprizma.uz/bahriddin/face-compare-api.git
   cd face-recognition-api
   ```

2. Install the required packages using pip and the provided `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the API:

   ```bash
   gunicorn -w 4 'main:app'
   ```

By default, the API will be available at `http://localhost:8000`.
And use configure nginx with nginx.conf 

## Usage

1. Send a POST request to the `/compare` endpoint.
2. Include the base64-encoded images in the request body as described in the [Compare Faces](#compare-faces) section.
3. Receive the comparison results in the response, indicating whether the faces match and additional timing information.

## Endpoints

### Check Server Status

#### `GET /`

Use this endpoint to check if the server is operational.

**Request:**

```http
GET /
```

**Response:**

- Status Code: 200 (OK)
- Body:

  ```json
  {
    "success": true,
    "message": "Server is working"
  }
  ```

### Compare Faces

#### `POST /compare`

This endpoint allows you to compare two faces and determine if they belong to the same person.

**Request:**

- Method: POST
- Endpoint: `/compare`
- Content-Type: application/json

**Request Body:**

```json
{
  "passport": "data:image/jpeg;base64,/9j/4AAQSkZ...",
  "face": "data:image/jpeg;base64,/9j/4AAQSkZ..."
}
```

- `passport`: Base64-encoded passport image data (JPEG or PNG)
- `face`: Base64-encoded face image data (JPEG or PNG)

**Response:**

- Status Code: 200 (OK)
- Body:

  ```json
  {
    "success": true,
    "match": true,
    "message": "It's the same person",
    "image_save_time": 0.12345,
    "comparison_time": 0.23456
  }
  ```

For more details on how to interpret the response, please refer to the [Response Format](#response-format) section.

## Response Format

The response from the API includes the following fields:

- `success`: A boolean indicating the success of the request.
- `match`: A boolean indicating whether the faces match.
- `message`: A message describing the comparison result.
- `image_save_time`: The time taken to save and preprocess the images (in seconds).
- `comparison_time`: The time taken to compare the faces (in seconds).

## Examples

Here are some example use cases:

1. **Check Server Status:**

   Send a GET request to `/`:

   ```http
   GET /
   ```

   Response:

   ```json
   {
     "success": true,
     "message": "Server is working"
   }
   ```

2. **Compare Faces:**

   Send a POST request to `/compare` with base64-encoded images:

   ```http
   POST /compare
   Content-Type: application/json

   {
     "passport": "data:image/jpeg;base64,/9j/4AAQSkZ...",
     "face": "data:image/jpeg;base64,/9j/4AAQSkZ..."
   }
   ```

   Response:

   ```json
   {
     "success": true,
     "match": true,
     "message": "It's the same person",
     "image_save_time": 0.12345,
     "comparison_time": 0.23456
   }
   ```

## Error Handling

- If the request data is invalid or the image format is incorrect, the API will respond with a `400 Bad Request` error.
- If an internal server error occurs during processing, the API will respond with a `500 Internal Server Error` error.

## Dependencies

- Flask
- face_recognition
