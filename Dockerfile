FROM python:3
WORKDIR /workdir 
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    codecov \
    flake8 \
    matplotlib \
    mutmut \
    mypy \
    numpy \
    pandas \
    pylint \
    pytest \
    pytest-cov \
    seaborn

RUN pip install git+https://github.com/genisott/pycondor.git
