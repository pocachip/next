package models

import (
	"errors"
	"time"
)

var _ = time.Thursday

//CrawlerJob
type CrawlerJob struct {
	Boundary  int        `gorm:"column:boundary" form:"boundary" json:"boundary" comment:"" sql:"tinyint"`
	Cat1Code  string     `gorm:"column:cat1_code" form:"cat1_code" json:"cat1_code" comment:"" sql:"varchar(10),MUL"`
	EndTime   *time.Time `gorm:"column:end_time" form:"end_time" json:"end_time,omitempty" comment:"" sql:"timestamp"`
	Id        uint       `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	Result    string     `gorm:"column:result" form:"result" json:"result" comment:"" sql:"varchar(32)"`
	StartTime *time.Time `gorm:"column:start_time" form:"start_time" json:"start_time,omitempty" comment:"" sql:"timestamp"`
	Website   int        `gorm:"column:website" form:"website" json:"website" comment:"" sql:"int,MUL"`
}

//TableName
func (m *CrawlerJob) TableName() string {
	return "crawler_job"
}

//One
func (m *CrawlerJob) One() (one *CrawlerJob, err error) {
	one = &CrawlerJob{}
	err = crudOne(m, one)
	return
}

//All
func (m *CrawlerJob) All(q *PaginationQuery) (list *[]CrawlerJob, total uint, err error) {
	list = &[]CrawlerJob{}
	total, err = crudAll(m, q, list)
	return
}

//Update
func (m *CrawlerJob) Update() (err error) {
	where := CrawlerJob{Id: m.Id}
	m.Id = 0

	return crudUpdate(m, where)
}

//Create
func (m *CrawlerJob) Create() (err error) {
	m.Id = 0

	return mysqlDB.Create(m).Error
}

//Delete
func (m *CrawlerJob) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
