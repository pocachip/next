package handlers

import (
	"rightwatch/models"
	"github.com/gin-gonic/gin"
)

func init() {
	groupApi.GET("check-list", checkListAll)
	groupApi.GET("check-list/:id",  checkListOne)
	groupApi.POST("check-list",  checkListCreate)
	groupApi.PATCH("check-list",  checkListUpdate)
	groupApi.DELETE("check-list/:id",  checkListDelete)
}
//All
func checkListAll(c *gin.Context) {
	mdl := models.CheckList{}
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
func checkListOne(c *gin.Context) {
	var mdl models.CheckList
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
func checkListCreate(c *gin.Context) {
	var mdl models.CheckList
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
func checkListUpdate(c *gin.Context) {
	var mdl models.CheckList
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
func checkListDelete(c *gin.Context) {
	var mdl models.CheckList
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
