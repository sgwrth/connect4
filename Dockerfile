FROM alpine:3.14
WORKDIR /connect4/src
COPY ./src/ .
RUN apk add --no-cache python3
CMD ["python3", "main.py"]
