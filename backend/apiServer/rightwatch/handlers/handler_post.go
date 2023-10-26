package handlers

import (
	"github.com/gin-gonic/gin"
	"rightwatch/models"
)

func init() {
	groupApi.GET("post", postAll)
	groupApi.GET("post/:id", postOne)
	groupApi.POST("post", postCreate)
	groupApi.PATCH("post", postUpdate)
	groupApi.DELETE("post/:id", postDelete)
}

//All
func postAll(c *gin.Context) {
	mdl := models.Post{}
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
func postOne(c *gin.Context) {
	var mdl models.Post
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
func postCreate(c *gin.Context) {
	var mdl models.Post
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
func postUpdate(c *gin.Context) {
	var mdl models.Post
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
func postDelete(c *gin.Context) {
	var mdl models.Post
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
