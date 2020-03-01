package controller

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-bongo/bongo"
	"gopkg.in/mgo.v2/bson"
	"iq-api-golang/main/model"
	"log"
	"net/http"
)

type Controller struct {
}

// NewController example
func NewController() *Controller {
	return &Controller{}
}

// ShowAccount godoc
// @Summary 아니 스웨거 자동 문서화가 아니야 ...
// @Description 주석으로 싹다 문서 작성해줘야되네 ... 근데 drf-yasg에서 문서 자동화한다고 더 어려워진 OAS구현체 파악한다고 짜치는거보다 차라리 이게 나을수도??
// @ID retrieve-person-with-name
// @Accept  json
// @Produce  json
// @Param name path string true "디폴트값"
// @Router /persons/{name} [get]
func (con *Controller) RetrieveOne(c *gin.Context) {

	config := &bongo.Config{
		ConnectionString: "root:1234@localhost:28817",
		Database:         "admin",
	}

	connection, err := bongo.Connect(config)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(c.Param("name"))
	results := connection.Collection("person").Find(bson.M{"Name": c.Param("name")})
	person := model.Person{}
	results.Next(person)

	c.JSON(http.StatusOK, person)
}
