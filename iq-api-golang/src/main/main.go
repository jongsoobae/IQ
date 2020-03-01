package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	controller "iq-api-golang/main/controller"
	_ "iq-api-golang/main/docs"
)

// @title Go Gin Iq API 문서
// @version 1.0
// @description 주석으로 API 문서를 만드네  흠터레스팅!
// @termsOfService http://swagger.io/terms/

// @contact.name 딜리버리히어로코리아 jongsu bae
// @contact.url http://www.swagger.io/support
// @contact.email 적당한 이메일 넣는곳

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host localhost
// @BasePath /
func main() {
	fmt.Println("asdf")

	r := gin.Default()

	ctl := controller.NewController()

	v1 := r.Group("/")
	{
		people := v1.Group("/persons")
		{
			people.GET("/:name", ctl.RetrieveOne)

			//...
		}
	}

	url := ginSwagger.URL("http://localhost:8080/swagger/doc.json") // The url pointing to API definition
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler, url))

	r.Run(":8080")

}
