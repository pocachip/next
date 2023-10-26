package models

import (
	"errors"
	"time"
)

var _ = time.Thursday

//SynonymWord
type SynonymWord struct {
	Id      uint   `gorm:"column:id" form:"id" json:"id" comment:"" sql:"int,PRI"`
	PairId  int    `gorm:"column:pair_id" form:"pair_id" json:"pair_id" comment:"" sql:"int,MUL"`
	Synonym string `gorm:"column:synonym" form:"synonym" json:"synonym" comment:"" sql:"varchar(128)"`
}

//TableName
func (m *SynonymWord) TableName() string {
	return "synonym_words"
}

//One
func (m *SynonymWord) One() (one *SynonymWord, err error) {
	one = &SynonymWord{}
	err = crudOne(m, one)
	return
}

//All
func (m *SynonymWord) All(q *PaginationQuery) (list *[]SynonymWord, total uint, err error) {
	list = &[]SynonymWord{}
	total, err = crudAll(m, q, list)
	return
}

//Update
func (m *SynonymWord) Update() (err error) {
	where := SynonymWord{Id: m.Id}
	m.Id = 0

	return crudUpdate(m, where)
}

//Create
func (m *SynonymWord) Create() (err error) {
	m.Id = 0

	return mysqlDB.Create(m).Error
}

//Delete
func (m *SynonymWord) Delete() (err error) {
	if m.Id == 0 {
		return errors.New("resource must not be zero value")
	}
	return crudDelete(m)
}
