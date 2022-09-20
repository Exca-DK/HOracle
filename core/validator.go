package core

import (
	"errors"
	"fmt"
	"log"
	"reflect"
	"sync"
	"sync/atomic"
)

type Incrementable interface {
	int64 | uint64 | int32 | uint32
}
type Decrementable interface {
	int64 | int32
}

type ICounter[t Incrementable] interface {
	Increment()
	Decrement()
	View() t
}

type Counter[t Incrementable] struct {
	value t
}

func (c *Counter[t]) Increment() {
	switch v := any(c.value).(type) {
	case int64:
		atomic.AddInt64(&v, 1)
	case int32:
		atomic.AddInt32(&v, 1)
	}
}

func (c *Counter[t]) Decrement() {
	switch v := any(c.value).(type) {
	case int64:
		atomic.AddInt64(&v, -1)
	case int32:
		atomic.AddInt32(&v, -1)
	}
}

func (c *Counter[t]) View() any {
	switch v := any(c.value).(type) {
	case int64:
		return atomic.LoadInt64(&v)
	case int32:
		return atomic.LoadInt32(&v)
	}
	return nil
}

type credentialFunc func(user string) (string, error)
type IValidator interface {
	Verify(key string, value string) error
}
type Validator struct {
	users   map[string]*User
	mu      sync.RWMutex
	fetcher credentialFunc
}

func (v *Validator) Verify(user string, password string) error {
	v.mu.RLock()
	defer v.mu.Unlock()
	_user, ok := v.users[user]

	if !ok {
		return fmt.Errorf("user %v does not exist", user)
	}

	psswd, err := _user.GetPassword()
	if err != nil {
		return err
	}

	if psswd != password {
		return errors.New("invalid credentials")
	}

	return nil
}

func (v *Validator) AddUser(user string) {
	v.mu.Lock()
	defer v.mu.Unlock()

	psswd, err := v.fetcher(user)
	if err != nil {
		log.Print(err)
	}

	if _, ok := v.users[user]; ok {
		return
	}

	u := NewUser()
	v.users[user] = &u
	v.users[user].UpdatePassword(psswd)
}

func NewValidator() *Validator {
	return &Validator{
		users: map[string]*User{},
		mu:    sync.RWMutex{},
	}
}

func ValidateBody(target interface{}) error {
	reflectType := reflect.TypeOf(target)
	reflectValue := reflect.ValueOf(target)
	if reflectType.Kind() == reflect.Pointer {
		reflectType = reflectType.Elem()
		reflectValue = reflectValue.Elem()
	}

	for i := 0; i < reflectType.NumField(); i++ {
		field := reflectValue.Field(i)
		valueValue := field.Interface()
		if field.IsZero() {
			msg := fmt.Sprintf("Missing field: %+v", reflectType.Field(i).Tag.Get("json"))
			return errors.New(msg)
		}

		switch field.Kind() {
		case reflect.Struct, reflect.Pointer:
			okay := ValidateBody(valueValue)
			if okay != nil {
				return okay
			}

		case reflect.Slice, reflect.Array:
			s := reflectValue.Field(i)
			for x := 0; x < s.Len(); x++ {
				okay := ValidateBody(s.Index(x).Interface())
				if okay != nil {
					return okay
				}
			}
		}
	}
	return nil
}
