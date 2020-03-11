package model

import (
	"github.com/go-bongo/bongo"
	"time"
)

type Person struct {
	bongo.DocumentBase `bson:",inline"`
	Name               string
	Date               time.Time
	Question           []string
}

type Question struct {
	bongo.DocumentBase `bson:",inline"`
	title              string
	content            string
}
