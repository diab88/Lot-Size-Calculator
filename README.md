# Flask Lot Size Calculator

This is a simple Flask web application that calculates the lot size based on the user's input for Capital Size, Risk Percentage, and Number of Stop Loss Points. The app is containerized using Docker for easy deployment.

## Features
- Takes Capital Size, Risk Percentage, and Stop Loss Points as inputs.
- Calculates and displays the appropriate lot size.
- Keeps the Capital Size and Risk Percentage after submission, while clearing the Stop Loss Points field.

## Technologies
- **Flask**: For the web application.
- **Docker**: To containerize and run the app in any environment.

### Running with Docker
- Build a Docker image and run the container. The app will be available on a specified port (e.g., 5000).

