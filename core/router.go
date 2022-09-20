package core

import (
	"net/http"

	"github.com/gorilla/mux"
)

type Router interface {
	Bind(path string, f func(http.ResponseWriter, *http.Request))
	Handle(path string, handler http.Handler)
	Handler() http.Handler
}

type ApiRouter struct {
	C *mux.Router
}

func (r *ApiRouter) Bind(path string, f func(http.ResponseWriter, *http.Request)) {
	r.C.HandleFunc(path, f)
}

func (r *ApiRouter) Handle(path string, handler http.Handler) {
	r.C.Handle(path, handler)
}

func (r *ApiRouter) Handler() http.Handler {
	return r.C
}

func NewRouter() Router {
	m := mux.NewRouter().StrictSlash(true)
	return &ApiRouter{C: m}
}
