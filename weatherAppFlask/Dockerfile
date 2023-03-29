FROM python:slim-buster
COPY deployApp/ /deployApp
WORKDIR /deployApp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "weatherAppFlask.py", "--host=0.0.0.0"]