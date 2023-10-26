package handlers

import (
	"github.com/gin-gonic/gin"
	"rightwatch/models"
)

func init() {
	groupApi.GET("synonym-word", synonymWordAll)
	groupApi.GET("synonym-word/:id", synonymWordOne)
	groupApi.POST("synonym-word", synonymWordCreate)
	groupApi.PATCH("synonym-word", synonymWordUpdate)
	groupApi.DELETE("synonym-word/:id", synonymWordDelete)
}

//All
func synonymWordAll(c *gin.Context) {
	mdl := models.SynonymWord{}
	query := &models.PaginationQuery{}
	err := c.ShouldBindQuery(query)
	if handleError(c, err) {
		return
	}
	list, total, err := mdl.All(query)
	if handleError(c, err) {
		return
	}
	jsonPagination(c, list, total, query)
}

//One
func synonymWordOne(c *gin.Context) {
	var mdl models.SynonymWord
	id, err := parseParamID(c)
	if handleError(c, err) {
		return
	}
	mdl.Id = id
	data, err := mdl.One()
	if handleError(c, err) {
		return
	}
	jsonData(c, data)
}

//Create
func synonymWordCreate(c *gin.Context) {
	var mdl models.SynonymWord
	err := c.ShouldBind(&mdl)
	if handleError(c, err) {
		return
	}
	err = mdl.Create()
	if handleError(c, err) {
		return
	}
	jsonData(c, mdl)
}

//Update
func synonymWordUpdate(c *gin.Context) {
	var mdl models.SynonymWord
	err := c.ShouldBind(&mdl)
	if handleError(c, err) {
		return
	}
	err = mdl.Update()
	if handleError(c, err) {
		return
	}
	jsonSuccess(c)
}

//Delete
func synonymWordDelete(c *gin.Context) {
	var mdl models.SynonymWord
	id, err := parseParamID(c)
	if handleError(c, err) {
		return
	}
	mdl.Id = id
	err = mdl.Delete()
	if handleError(c, err) {
		return
	}
	jsonSuccess(c)
}
