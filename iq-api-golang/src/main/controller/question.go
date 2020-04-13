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

// FindAllQuestion godoc
// @ID FindAll-Question
// @Summary 아니 스웨거 자동 문서화가 아니야 ...
// @Description 주석으로 싹다 문서 작성해줘야되네 ...
// @Accept  json
// @Produce  json
// @Success 200 {array} model.Questions
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /questions [get]
func (con *Controller) FindAllQuestion(c *gin.Context) {

	connection := core.GetMongoConnection()

	results := connection.Collection("questions").Find(bson.M{})

	var question = &model.Questions{}
	var questionList []model.Questions

	for results.Next(question) {
		questionList = append(questionList, *question)
	}
	fmt.Println(questionList, ".....")

	c.JSON(http.StatusOK, questionList)
}

// CreateQuestion godoc
// @ID Create-Questions
// @Summary 이건 Questions 생성 API
// @Description  자동화가 안되서 슬픈 문서여..
// @Accept  json
// @Produce  json
// @Param question body model.Questions true "Questions"
// @Success 200 {object} httputil.QuestionHTTPSuccess
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /questions [post]
func (con *Controller) CreateQuestion(c *gin.Context) {
	var question model.Questions
	c.BindJSON(&question)

	connection := core.GetMongoConnection()
	err := connection.Collection("questions").Save(&question)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", question)

	c.JSON(http.StatusOK, gin.H{
		"msg":  "created",
		"data": question,
	})
}

// UpdateQuestion godoc
// @ID Update-Questions
// @Summary 이건 Questions 수정 API
// @Description  자동화가 안되서 슬픈 문서여..
// @Accept  json
// @Produce  json
// @Param id path string true "Question ID"
// @Param question body model.Questions true "Questions"
// @Success 200 {object} httputil.HTTPSuccess
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Failure 500 {object} httputil.HTTPError
// @Router /questions/{id} [put]
func (con *Controller) UpdateQuestion(c *gin.Context) {
	var question model.Questions
	c.BindJSON(&question)

	modifiedQuestion := model.Questions{DocumentBase: model.DocumentBase{Id: question.Id}, Title: question.Title, Content: question.Content}

	connection := core.GetMongoConnection()
	err := connection.Collection("questions").Save(&modifiedQuestion)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", question)

	c.JSON(http.StatusOK, gin.H{
		"msg": "updated",
	})
}

// DeleteQuestion godoc
// @ID Delete-Question
// @Summary 이건 Question 삭제API
// @Description  ....
// @Accept  json
// @Produce  json
// @Param id path string true "Question ID"
// @Success 200 {object} httputil.HTTPSuccess
// @Failure 400 {object} httputil.HTTPError
// @Failure 404 {object} httputil.HTTPError
// @Router /questions/{id} [delete]
func (con *Controller) DeleteQuestion(c *gin.Context) {

	idStr := c.Param("id")

	connection := core.GetMongoConnection()
	err := connection.Collection("questions").DeleteOne(bson.M{"_id": bson.ObjectIdHex(idStr)})

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "그 Question은 없는데?(이미 삭제된건가?)",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "deleted",
	})
}
