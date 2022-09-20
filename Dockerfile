FROM golang:1.19.0 as go

WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
COPY prometheus/prometheus.yml /etc/prometheus/config
RUN go build -o bin

ENTRYPOINT ["/app/bin"]