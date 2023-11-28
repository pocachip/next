package models

import (
	"errors"
	"time"
)

var _ = time.Thursday

// Post
type Screenshots struct {
	Url    string `gorm:"column:url" form:"url" json:"url" comment:"" sql:"varchar(128)"`
	UrlMd5 string `gorm:"column:url_md5" form:"url_md5" json:"url_md5" comment:"" sql:"varchar(32)"`
	Ts     string `gorm:"column:ts" form:"ts" json:"ts" comment:"" sql:"varchar(256)"`
}

// TableName
func (m *Screenshots) TableName() string {
	return "screenshots"
}

// One
func (m *Screenshots) One() (one *Screenshots, err error) {
	one = &Screenshots{}
	err = crudOne(m, one)
	return
}

// All
func (m *Screenshots) All(q *PaginationQuery) (list *[]Screenshots, total uint, err error) {
	list = &[]Screenshots{}
	total, err = crudAll(m, q, list)
	return
}

// Update
func (m *Screenshots) Update() (err error) {
	where := Screenshots{UrlMd5: m.UrlMd5}
	m.UrlMd5 = ""

	return crudUpdate(m, where)
}

// Create
func (m *Screenshots) Create() (err error) {
	m.UrlMd5 = ""

	return mysqlDB.Create(m).Error
}

// Delete
func (m *Screenshots) Delete() (err error) {
	if m.UrlMd5 == "" {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
