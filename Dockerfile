FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir pdf
RUN mkdir -p assets/comprovantes
RUN mkdir -p assets/rpa

COPY . .

CMD [ "python", "./bot.py" ]