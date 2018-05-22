FROM python:3.6-alpine

COPY ./ /SmartLib

WORKDIR /SmartLib
RUN pip install -r requirements.txt && pip install gunicorn

EXPOSE 8000

CMD [ "gunicorn", "-w", "2", "-b", "0.0.0.0", "app:app" ]
