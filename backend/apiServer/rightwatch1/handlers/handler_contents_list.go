package handlers

import (
	"rightwatch1/models"
	"github.com/gin-gonic/gin"
)

func init() {
	groupApi.GET("contents-list", contentsListAll)
	groupApi.GET("contents-list/:id",  contentsListOne)
	groupApi.POST("contents-list",  contentsListCreate)
	groupApi.PATCH("contents-list",  contentsListUpdate)
	groupApi.DELETE("contents-list/:id",  contentsListDelete)
}
//All
func contentsListAll(c *gin.Context) {
	mdl := models.ContentsList{}
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
func contentsListOne(c *gin.Context) {
	var mdl models.ContentsList
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
func contentsListCreate(c *gin.Context) {
	var mdl models.ContentsList
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
func contentsListUpdate(c *gin.Context) {
	var mdl models.ContentsList
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
func contentsListDelete(c *gin.Context) {
	var mdl models.ContentsList
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
