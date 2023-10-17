package models

import (
	"errors"
	"time"
	
)

var _ = time.Thursday
//ContentsList
type ContentsList struct {
	
	Id   uint     `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	Title   string     `gorm:"column:title" form:"title" json:"title" comment:"" sql:"varchar(256)"`
}
//TableName
func (m *ContentsList) TableName() string {
	return "contents_list"
}
//One
func (m *ContentsList) One() (one *ContentsList, err error) {
	one = &ContentsList{}
	err = crudOne(m, one)
	return
}
//All
func (m *ContentsList) All(q *PaginationQuery) (list *[]ContentsList, total uint, err error) {
	list = &[]ContentsList{}
	total, err = crudAll(m, q, list)
	return
}
//Update
func (m *ContentsList) Update() (err error) {
	where := ContentsList{Id: m.Id}
	m.Id = 0
	
	return crudUpdate(m, where)
}
//Create
func (m *ContentsList) Create() (err error) {
	m.Id = 0
    
	return mysqlDB.Create(m).Error
}
//Delete
func (m *ContentsList) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
