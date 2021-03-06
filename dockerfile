FROM python:3.8
RUN adduser -disabled-login myuser
USER myuser
WORKDIR /home/myuser
COPY --chown=myuser:myuser requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

COPY --chown=myuser:myuser . .

EXPOSE 5001

CMD [ "python", "./server.py" ]