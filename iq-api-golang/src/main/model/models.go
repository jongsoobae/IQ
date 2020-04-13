package model

type Persons struct {
	DocumentBase `bson:",inline"`
	Name         string `json:"name" binding:"required" example:"김응시자"`
	//Date               string `form:"date" json:"date" xml:"date" example:"2020-03-02 11:04:05"`
	Question []string `json:"question" example:"1+1은 무엇입니까?"`

	//CreatedOn int64         `json:"created_on" bson:"created_on"`
	//UpdatedOn int64         `json:"updated_on" bson:"updated_on"`
}

type Questions struct {
	DocumentBase `bson:",inline"`
	Title        string `json:"title" bson:"title" binding:"required" example:"1+1은 무엇입니까?"`
	Content      string `json:"content" bson:"content" binding:"required" example:"1더하기1을 3이라 대답함! 성장가능성을 확인함..."`
}
