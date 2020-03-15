package controller

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"gopkg.in/mgo.v2/bson"
	"iq-api-golang/core"
	"iq-api-golang/model"
	"log"
	"net/http"
)

type Controller struct {
}

// NewController example
func NewController() *Controller {
	return &Controller{}
}

// FindOnePerson godoc
// @ID FindOne-Person
// @Summary 면접자 불러오기
// @Description 주...
// @Param id path string true "Person ID"
// @Accept  json
// @Produce  json
// @Success 200 {object} model.Persons
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /persons/{id} [get]
func (con *Controller) FindOnePerson(c *gin.Context) {

	idStr := c.Param("id")
	person := &model.Persons{}

	connection := core.GetMongoConnection()

	err := connection.Collection("persons").FindById(bson.ObjectIdHex(idStr), person)

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "그 Person은 없는데?",
		})
		return
	}

	fmt.Println(person, ".....")

	c.JSON(http.StatusOK, person)
}

// FindAllPerson godoc
// @ID FindAll-Person
// @Summary 아니 스웨거 자동 문서화가 아니야 ...
// @Description 주석으로 싹다 문서 작성해줘야되네 ... 근데 drf-yasg에서 문서 자동화한다고 더 어려워진 OAS구현체 파악한다고 짜치는거보다 차라리 이게 나을수도??
// @Accept  json
// @Produce  json
// @Success 200 {array} model.Persons
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /persons [get]
func (con *Controller) FindAllPerson(c *gin.Context) {

	connection := core.GetMongoConnection()

	results := connection.Collection("persons").Find(bson.M{})

	var person = &model.Persons{}
	var personList []model.Persons

	for results.Next(person) {
		personList = append(personList, *person)
	}
	fmt.Println(personList, ".....")

	c.JSON(http.StatusOK, personList)
}

// CreatePerson godoc
// @ID Create-Person
// @Summary 이건 생성API
// @Description  자동화가 안되서 슬픈 문서여..
// @Accept  json
// @Produce  json
// @Param person body model.Persons true "Person"
// @Success 200 {object} model.Persons
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /persons [post]
func (con *Controller) CreatePerson(c *gin.Context) {
	var person model.Persons
	c.BindJSON(&person)

	connection := core.GetMongoConnection()
	err := connection.Collection("persons").Save(&person)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", person)

	c.JSON(http.StatusOK, gin.H{
		"msg": "created",
	})
}

// DeletePerson godoc
// @ID Delete-Person
// @Summary 이건 삭제API
// @Description  ....
// @Accept  json
// @Produce  json
// @Param id path string true "Person ID"
// @Success 200 {object} httputil.HTTPSuccess
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Router /persons/{id} [delete]
func (con *Controller) DeletePerson(c *gin.Context) {

	idStr := c.Param("id")

	//if validationCheck == false{
	//	httputil.CustomError(c, http.StatusBadRequest,"id를 입력해주세요.")
	//	return
	//}

	connection := core.GetMongoConnection()
	err := connection.Collection("persons").DeleteOne(bson.M{"_id": bson.ObjectIdHex(idStr)})

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "그 Person은 없는데?(이미 삭제된건가?)",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "deleted",
	})
}
