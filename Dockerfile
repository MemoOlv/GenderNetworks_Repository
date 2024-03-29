FROM python:3
WORKDIR /workdir 
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    codecov \
    flake8 \
    mutmut \
    mypy \
    pylint \
    pytest \
    pytest-cov \
    pandas \
    seaborn \
    numpy \
    matplotlib

RUN pip install git+https://github.com/genisott/pycondor.git
