package core

import (
	"errors"
	"sync"
)

type IStack[T any] interface {
	PopRight() (T, error)
	PopLeft() (T, error)
	Push(v T)
	Size() int
}

type Stack[T any] []T

func (s *Stack[T]) Push(v T) {
	*s = append(*s, v)
}

func (s *Stack[T]) ViewLeft() (T, error) {
	ss := *s
	if len(ss) == 0 {
		return *new(T), errors.New("cant view from empty stack")
	}
	ele := ss[0]
	return ele, nil
}

func (s *Stack[T]) ViewRight() (T, error) {
	ss := *s
	l := len(ss)
	if len(ss) == 0 {
		return *new(T), errors.New("cant view from empty stack")
	}
	ele := ss[l-1]
	return ele, nil
}

func (s *Stack[T]) PopRight() (T, error) {
	ss := *s
	l := len(ss)
	if len(ss) == 0 {
		return *new(T), errors.New("cant pop from empty stack")
	}
	ele := ss[l-1]
	*s = ss[:l-1]
	return ele, nil
}

func (s *Stack[T]) PopLeft() (T, error) {
	ss := *s
	if len(ss) == 0 {
		return *new(T), errors.New("cant pop from empty stack")
	}
	ele := ss[0]
	*s = ss[:1]
	return ele, nil
}

func (s *Stack[T]) Size() int {
	return len(*s)
}

func NewStack[T any]() Stack[T] {
	return make(Stack[T], 0)
}

type StackThreadSafe[T any] struct {
	inner IStack[T]
	mutex sync.Mutex
}

func (t *StackThreadSafe[T]) Push(v T) {
	t.mutex.Lock()
	defer t.mutex.Unlock()
	t.inner.Push(v)
}

func (t *StackThreadSafe[T]) PopRight() (T, error) {
	t.mutex.Lock()
	defer t.mutex.Unlock()
	item, err := t.inner.PopRight()
	if err != nil {
		return item, err
	}
	return item, nil
}

func (t *StackThreadSafe[T]) PopLeft() (T, error) {
	t.mutex.Lock()
	defer t.mutex.Unlock()
	item, err := t.inner.PopLeft()
	if err != nil {
		return item, err
	}
	return item, nil
}

func (t *StackThreadSafe[T]) Size() int {
	t.mutex.Lock()
	defer t.mutex.Unlock()
	return t.inner.Size()
}

func NewThreadsafeStack[T any]() *StackThreadSafe[T] {
	st := make(Stack[T], 0)
	return &StackThreadSafe[T]{inner: &st}
}
