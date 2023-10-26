package models

import (
	"errors"
	"time"
)

var _ = time.Thursday

//KtaContent
type KtaContent struct {
	Id       uint   `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	Genre    string `gorm:"column:genre" form:"genre" json:"genre" comment:"" sql:"varchar(256)"`
	Title    string `gorm:"column:title" form:"title" json:"title" comment:"" sql:"varchar(256)"`
	Actors   string `gorm:"column:actors" form:"actors" json:"actors" comment:"" sql:"text"`
	Director string `gorm:"column:director" form:"director" json:"director" comment:"" sql:"varchar(256)"`
	Price    string `gorm:"column:price" form:"price" json:"price" comment:"" sql:"varchar(256)"`
	Enddate  string `gorm:"column:enddate" form:"enddate" json:"enddate" comment:"" sql:"varchar(256)"`
	Synop    string `gorm:"column:synop" form:"synop" json:"synop" comment:"" sql:"text"`
	PUrl     string `gorm:"column:p_url" form:"p_url" json:"p_url" comment:"" sql:"varchar(256)"`
}

//TableName
func (m *KtaContent) TableName() string {
	return "kta_contents"
}

//One
func (m *KtaContent) One() (one *KtaContent, err error) {
	one = &KtaContent{}
	err = crudOne(m, one)
	return
}

//All
func (m *KtaContent) All(q *PaginationQuery) (list *[]KtaContent, total uint, err error) {
	list = &[]KtaContent{}
	total, err = crudAll(m, q, list)
	return
}

//Update
func (m *KtaContent) Update() (err error) {
	where := KtaContent{Id: m.Id}
	m.Id = 0

	return crudUpdate(m, where)
}

//Create
func (m *KtaContent) Create() (err error) {
	m.Id = 0

	return mysqlDB.Create(m).Error
}

//Delete
func (m *KtaContent) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
