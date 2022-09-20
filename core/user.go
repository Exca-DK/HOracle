package core

import (
	"time"
)

type User struct {
	name     string
	activity Stack[time.Time]
	psswd    Stack[string]
	counter  Counter[int32]
}

func (u *User) GetName() string {
	return u.name
}

func (u *User) IncreaseAttempt() {
	u.counter.Increment()
}

func (u *User) DecreaseAttempt() {
	u.counter.Decrement()
}

func (u *User) GetPassword() (string, error) {
	return u.psswd.ViewRight()
}

func (u *User) UpdatePassword(psswd string) {
	u.psswd.Push(psswd)
	u.activity.Push(time.Now())
}

func NewUser() User {
	return User{}
}
