package models

import (
	"errors"
	"time"
	
)

var _ = time.Thursday
//CheckList
type CheckList struct {
	
	ContentId   string     `gorm:"column:content_id" form:"content_id" json:"content_id" comment:"" sql:"varchar(256),MUL"`
	FirstTime   *time.Time     `gorm:"column:first_time" form:"first_time" json:"first_time,omitempty" comment:"" sql:"timestamp"`
	Id   uint     `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	PostId   string     `gorm:"column:post_id" form:"post_id" json:"post_id" comment:"" sql:"varchar(256)"`
	PostIdx   string     `gorm:"column:post_idx" form:"post_idx" json:"post_idx" comment:"" sql:"varchar(256)"`
	PostTxt   string     `gorm:"column:post_txt" form:"post_txt" json:"post_txt" comment:"" sql:"varchar(256)"`
	Status   int     `gorm:"column:status" form:"status" json:"status" comment:"" sql:"tinyint"`
	UpdateTime   *time.Time     `gorm:"column:update_time" form:"update_time" json:"update_time,omitempty" comment:"" sql:"timestamp"`
}
//TableName
func (m *CheckList) TableName() string {
	return "check_list"
}
//One
func (m *CheckList) One() (one *CheckList, err error) {
	one = &CheckList{}
	err = crudOne(m, one)
	return
}
//All
func (m *CheckList) All(q *PaginationQuery) (list *[]CheckList, total uint, err error) {
	list = &[]CheckList{}
	total, err = crudAll(m, q, list)
	return
}
//Update
func (m *CheckList) Update() (err error) {
	where := CheckList{Id: m.Id}
	m.Id = 0
	
	return crudUpdate(m, where)
}
//Create
func (m *CheckList) Create() (err error) {
	m.Id = 0
    
	return mysqlDB.Create(m).Error
}
//Delete
func (m *CheckList) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
