FROM python:3.6-alpine

COPY ./ /SmartLib

WORKDIR /SmartLib
RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt && \
 pip install gunicorn && \
 apk --purge del .build-deps


EXPOSE 8000

CMD [ "gunicorn", "-w", "2", "-b", "0.0.0.0", "app:app" ]
