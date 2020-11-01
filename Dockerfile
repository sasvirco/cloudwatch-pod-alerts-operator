FROM python:3.7
ADD /src/handler.py app.py
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD kopf run app.py
