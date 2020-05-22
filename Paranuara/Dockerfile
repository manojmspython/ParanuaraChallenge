FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /Paranuara
WORKDIR /Paranuara
COPY . /Paranuara/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader wordnet
RUN bash -c "python manage.py makemigrations && python manage.py migrate"

EXPOSE 5000