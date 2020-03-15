package httputil

import (
	"github.com/gin-gonic/gin"
	"iq-api-golang/model"
)

// 이렇게 구조체 만들어서 문서 정의시 아래 객체들을 response로 등록한다
// swaggo 예제에서 쓰는 방식임 https://github.com/swaggo/swag/blob/master/example/celler/httputil/error.go
func CustomError(ctx *gin.Context, status int, message string) {
	er := HTTPError{
		Code:    status,
		Message: message,
	}
	ctx.JSON(status, er)
}

// HTTPError
type HTTPError struct {
	Code    int    `json:"code" example:"400"`
	Message string `json:"msg" example:"잘못된 입력입니다."`
}

// HTTPSuccess
type HTTPSuccess struct {
	Code    int    `json:"code" example:"200"`
	Message string `json:"msg" example:"처리되었습니다."`
}

type QuestionHTTPSuccess struct {
	Code    int             `json:"code" example:"200"`
	Message string          `json:"msg" example:"처리되었습니다."`
	Data    model.Questions `json:"data"`
}
