package internal

import (
	"errors"
	"fmt"
	"net"
	"net/http"
)

type IValidator interface {
	Verify(key string, value string) error
}

func ValidateRequest(r *http.Request, target interface{}) (bool, error) {
	ctHdr := r.Header.Get("Content-Type")
	if ctHdr != "application/json" {
		return false, errors.New("only application/json")
	}
	return true, nil
}

func ValidateToken(r *http.Request, v interface{}) (bool, error) {
	tokenString := r.Header.Get("token")
	_, err := verifyToken(tokenString)
	if err != nil {
		return false, err
	}
	return true, nil
}

func ValidateUser(r *http.Request, v interface{}) (bool, error) {
	user := r.Header.Get("user")
	password := r.Header.Get("password")
	if len(user) == 0 || len(password) == 0 {
		return false, errors.New("invalid auth")
	}
	err := v.(IValidator).Verify(user, password)
	if err != nil {
		return false, err
	}
	return true, nil
}

func ParseIp(remote string) (net.IP, error) {
	ip, _, err := net.SplitHostPort(remote)
	if err != nil {
		//return nil, fmt.Errorf("userip: %q is not IP:port", req.RemoteAddr)

		return nil, fmt.Errorf("userip: %q is not IP:port", remote)
	}

	userIP := net.ParseIP(ip)
	if userIP == nil {
		//return nil, fmt.Errorf("userip: %q is not IP:port", req.RemoteAddr)
		return nil, fmt.Errorf("userip: %q is not IP:port", remote)
	}
	return userIP, nil
}
