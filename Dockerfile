FROM python:3.12
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8

RUN pip install \
    matplotlib \
    numpy \
    pandas \
    scipy \
    seaborn
