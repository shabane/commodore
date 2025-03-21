FROM python:alpine
RUN apk add entr
COPY . /code
WORKDIR /code
RUN pip install -r /code/requirements.txt
ENV PROMPTS_FILE=prompts.yaml
CMD [ "/code/runner.sh" ]