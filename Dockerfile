FROM tiangolo/uvicorn-gunicorn:python3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/local/lib/python3.8/

ENV APP_ROOT /src

RUN mkdir ${APP_ROOT};

WORKDIR ${APP_ROOT}

COPY ./requirements.txt /config/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /config/requirements.txt

ADD src ${APP_ROOT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8087"]
