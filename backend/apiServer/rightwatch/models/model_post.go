package models

import (
	"errors"
	"time"
)

var _ = time.Thursday

//Post
type Post struct {
	Id             uint   `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	Website        int    `gorm:"column:website" form:"website" json:"website" comment:"" sql:"int"`
	Cat1Code       string `gorm:"column:cat1_code" form:"cat1_code" json:"cat1_code" comment:"" sql:"varchar(10)"`
	Cat2Code       string `gorm:"column:cat2_code" form:"cat2_code" json:"cat2_code" comment:"" sql:"varchar(10)"`
	Cat1Title      string `gorm:"column:cat1_title" form:"cat1_title" json:"cat1_title" comment:"" sql:"varchar(30)"`
	Cat2Title      string `gorm:"column:cat2_title" form:"cat2_title" json:"cat2_title" comment:"" sql:"varchar(30)"`
	Idx            string `gorm:"column:idx" form:"idx" json:"idx" comment:"" sql:"varchar(128)"`
	Txt            string `gorm:"column:txt" form:"txt" json:"txt" comment:"" sql:"varchar(256),MUL"`
	Lvl19          string `gorm:"column:lvl19" form:"lvl19" json:"lvl19" comment:"" sql:"varchar(128)"`
	Price          string `gorm:"column:price" form:"price" json:"price" comment:"" sql:"varchar(128)"`
	Seller         string `gorm:"column:seller" form:"seller" json:"seller" comment:"" sql:"varchar(128)"`
	Partner        string `gorm:"column:partner" form:"partner" json:"partner" comment:"" sql:"varchar(128)"`
	AttachFileSize string `gorm:"column:attach_file_size" form:"attach_file_size" json:"attach_file_size" comment:"" sql:"varchar(256)"`
	ItemUrl        string `gorm:"column:item_url" form:"item_url" json:"item_url" comment:"" sql:"varchar(256)"`
	LastUpdate     string `gorm:"column:last_update" form:"last_update" json:"last_update" comment:"" sql:"varchar(256)"`
}

//TableName
func (m *Post) TableName() string {
	return "post"
}

//One
func (m *Post) One() (one *Post, err error) {
	one = &Post{}
	err = crudOne(m, one)
	return
}

//All
func (m *Post) All(q *PaginationQuery) (list *[]Post, total uint, err error) {
	list = &[]Post{}
	total, err = crudAll(m, q, list)
	return
}

//Update
func (m *Post) Update() (err error) {
	where := Post{Id: m.Id}
	m.Id = 0

	return crudUpdate(m, where)
}

//Create
func (m *Post) Create() (err error) {
	m.Id = 0

	return mysqlDB.Create(m).Error
}

//Delete
func (m *Post) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
