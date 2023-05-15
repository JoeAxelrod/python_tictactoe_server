FROM python:3.9-slim

WORKDIR /app

COPY tictactoe/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tictactoe /app/tictactoe
COPY tictactoe/flask_app.py .

# Use Gunicorn as the WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:5007", "flask_app:app"]



# docker build -t tictactoe .
# docker run -d -p 5007:5007 tictactoe
# curl -X POST -d '{"phone":"654654654", "action": "0 2"}' -H "Content-Type: application/json" http://localhost:5007/api/tictactoe -v
