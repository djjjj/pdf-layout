FROM python:3.12
COPY sources.list /etc/apt/sources.list
COPY pip.conf /root/.pip/pip.conf

WORKDIR /app

ADD pdm.lock /app
ADD pyproject.toml /app
ADD .env /app
ADD app /app/app

ENV PATH="/app/.venv/bin:$PATH"
RUN pip install pdm && pdm install

