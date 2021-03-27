FROM python
COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install "poetry==1.0.0"
COPY .. /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 3306
CMD python /app/Python_Trade_Bot.py