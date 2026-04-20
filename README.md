# Musical Eras Learning App

This repository contains a Flask web application for a UI design class project. The app teaches users to recognize Baroque, Classical, and Romantic musical eras through embedded audio lessons and an interactive quiz.

## Features

- Flask backend with JSON-driven lesson and quiz data
- Bootstrap and jQuery frontend
- Home page with start button
- Learning flow with three lesson screens
- Quiz flow with multiple-choice questions and scoring
- Results page with score summary and answer review

## Run locally

1. Create and activate a Python virtual environment.

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app.

   ```powershell
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000/`.

## Project structure

- `app.py` — Flask routes and session tracking
- `content.json` — lesson and quiz content data
- `templates/` — HTML templates for the app
- `static/css/style.css` — custom styling
