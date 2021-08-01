# manim-server

This application serves client [Manim Interactive (github.com/awtotty/manimi)](https://github.com/awtotty/manimi) instances in their requests for scenes rendered my [Manim (manim.community](https://www.manim.community/). 

## Installation
To run the server, install the dependencies: 
```pip install Flask==1.1.2 Flask-Cors==3.0.10```

Docker is required to run the Manim renderer. For Ubuntu, run
```sudo apt install docker.io```
and add the user to the docker group
```sudo usermod -a -G docker $USER```

If you are not using Ubuntu, [install Docker](https://docs.docker.com/engine/install/) using the available package manager. (_Note: this server is currently only supported on Linux_). 

## Run
Run the server with your preferred production server (e.g. gunicorn, nginx, etc.) or on a development server with 
```python app.py```
