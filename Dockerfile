FROM python:3
WORKDIR /workdir 
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    codecov \
    flake8 \
    mutmut \
    pylint \
    pytest \
    pytest-cov

RUN pip install git+https://github.com/genisott/pycondor.git

RUN make install
