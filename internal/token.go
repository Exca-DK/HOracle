package internal

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v4"
)

func GenerateNewToken(issuer string, addresser string) (string, error) {
	claimsMap := jwt.MapClaims{
		"iss":  issuer,
		"adds": addresser,
		"exp":  time.Now().Add(24 * time.Hour).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claimsMap)
	//#TODO secret should be fetched from env file
	tokenString, err := token.SignedString("secret")
	return tokenString, err
}

func verifyToken(tokenString string) (*jwt.Token, error) {
	splitToken := strings.Split(tokenString, ".")
	// if length is not 3, we know that the token is corrupt
	if len(splitToken) != 3 {
		return nil, errors.New("invalid token")
	}
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		//Make sure that the token method conform to "SigningMethodHMAC"
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte("secret"), nil
	})
	if err != nil {
		return nil, err
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return nil, errors.New("invalid token")
	}
	exp, ok := claims["exp"].(string)
	if !ok {
		return nil, errors.New("invalid token")
	}
	value, _ := strconv.Atoi(exp)
	deadline := time.Unix(int64(value), 0)
	if time.Since(deadline) > 0 {
		return nil, errors.New("token expired")
	}
	return token, nil
}
