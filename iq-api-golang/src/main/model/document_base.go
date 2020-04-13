package model

import (
	"gopkg.in/mgo.v2/bson"
	"time"
)

type DocumentBase struct {
	Id       bson.ObjectId `bson:"_id,omitempty" json:"id" example:"5e6ddd933070909e680d33a6"`
	Created  time.Time     `bson:"_created" json:"_created" example:"2020-03-15T07:45:26.085Z"`
	Modified time.Time     `bson:"_modified" json:"_modified" example:"2020-03-15T07:45:26.085Z"`

	exists bool
}

// Mongo 기존 필드 Getter & Setter

func (d *DocumentBase) SetIsNew(isNew bool) {
	d.exists = !isNew
}

func (d *DocumentBase) IsNew() bool {
	return !d.exists
}

func (d *DocumentBase) GetId() bson.ObjectId {
	return d.Id
}

func (d *DocumentBase) SetId(id bson.ObjectId) {
	d.Id = id
}

func (d *DocumentBase) SetCreated(t time.Time) {
	d.Created = t
}

func (d *DocumentBase) SetModified(t time.Time) {
	d.Modified = t
}
