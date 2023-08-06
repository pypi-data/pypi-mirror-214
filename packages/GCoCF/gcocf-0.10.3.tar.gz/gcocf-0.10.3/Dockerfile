FROM python:3.11
RUN pip install --no-cache-dir --upgrade pip flit

ENV FLIT_ROOT_INSTALL=1
WORKDIR /app

ADD pyproject.toml .
ADD LICENSE.txt .
ADD README.md .
ADD GCoCF ./GCoCF
RUN flit install

ENV LC_ALL=C.UTF-8
WORKDIR /app
ENTRYPOINT ["GCoCF"]


