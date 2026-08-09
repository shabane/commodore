FROM python:3.11-slim
RUN apt-get update && apt-get install -y entr
COPY . /code
WORKDIR /code
RUN pip install -r /code/requirements.txt
ENV PROMPTS_FILE=prompts.yaml
CMD [ "/code/runner.sh" ]