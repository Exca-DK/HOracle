package core

import (
	"context"
)

type Services []Service

type Response struct {
	Code  int         `json:"code"`
	Error error       `json:"error,omitempty"`
	Data  interface{} `json:"data,omitempty"`
}

type Request interface{}

type GetRequest Request
type GetResponse Response

type PostRequest Request
type PostResponse Response

type StatusRequest Request
type StatusResponse Response

type Service interface {
	Post(ctx context.Context, request PostRequest) PostResponse
	Get(ctx context.Context, request GetRequest) GetResponse
	Status(ctx context.Context, request StatusRequest) StatusResponse
	Name() string
	Path() string
}
