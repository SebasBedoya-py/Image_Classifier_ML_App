# Image classifier ML App

## Overview

This project is a machine learning application built with FastAPI that automatically classifies images into over 1000 different categories using a pre-trained Convolutional Neural Network (CNN) implemented in TensorFlow. The application features a web user interface where users can upload images and receive predictions from the model.

## Table of Contents

- [Business Problem](#business-problem)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Business Problem

Imagine a company with a large collection of images that needs to classify them into different categories automatically. This task can be time-consuming and error-prone when done manually. This application aims to streamline that process by leveraging machine learning.

## Technologies Used

- **Python**: Main programming language
- **FastAPI**: Framework for building the API
- **Streamlit**: Framework for the web UI
- **TensorFlow**: For loading the pre-trained CNN model
- **Redis**: For communication between microservices
- **Docker**: For containerization
- **Locust**: For stress testing the solution

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Copy the environment variables:
    ```bash
    cp .env.original .env

3. Create Docker network:
    ```bash
    docker network create shared_network

4. Build the Docker images and run the containers (Services):
    ```bash
    docker-compose up --build -d

## Usage
Access the FastAPI documentation at http://localhost:8000/docs to explore the API endpoints.
Access the web UI at http://localhost:9090 to upload images and view predictions.

Login Credentials for UI
Username: admin@example.com
Password: admin

## API Documentation
The API provides several endpoints for user authentication, image classification, and feedback submission. You can find detailed documentation at the FastAPI docs URL mentioned above.