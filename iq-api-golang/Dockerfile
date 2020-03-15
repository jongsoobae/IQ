FROM golang:1.14-alpine AS builder


RUN apk update && apk add alpine-sdk git && rm -rf /var/cache/apk/*
RUN apk --no-cache add gcc g++ make git

COPY ./src /iq-api-golang/src

WORKDIR /iq-api-golang/src

RUN go mod download

RUN go build
RUN GOOS=linux go build -ldflags="-s -w" -o ./bin/web-app ./main.go

FROM alpine:3.9
RUN apk --no-cache add ca-certificates
WORKDIR /usr/bin
COPY --from=build /go/src/app/bin /go/bin
EXPOSE 80
ENTRYPOINT /go/bin/web-app --port 80