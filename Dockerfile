FROM python

WORKDIR /project

COPY . /project

RUN pip install -U pip

RUN pip install -r requirments.txt

EXPOSE 8000

CMD ["gunicorn","A.wsgi","*:8000"]
