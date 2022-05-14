FROM python:3.9

WORKDIR /cart

COPY ./README.md /cart/README.md

COPY ./requirements.txt /cart/requirements.txt

COPY ./.env /cart/.env

COPY ./config.py /cart/config.py

COPY ./setup.py /cart/setup.py

COPY ./app /cart/app

RUN pip install -e /cart/.

CMD ["python", "/cart/app/main.py"]
