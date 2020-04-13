package core

import (
	"github.com/go-bongo/bongo"
	"log"
)

func GetMongoConnection() *bongo.Connection {
	config := &bongo.Config{
		ConnectionString: "root:root@127.0.0.1:27017",
		Database:         "iqdb",
	}

	connection, err := bongo.Connect(config)

	if err != nil {
		log.Fatal(err)
	}
	return connection
}
