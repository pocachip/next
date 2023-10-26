package handlers

import (
	"github.com/gin-gonic/gin"
	"rightwatch/models"
)

func init() {
	groupApi.GET("kta-content", ktaContentAll)
	groupApi.GET("kta-content/:id", ktaContentOne)
	groupApi.POST("kta-content", ktaContentCreate)
	groupApi.PATCH("kta-content", ktaContentUpdate)
	groupApi.DELETE("kta-content/:id", ktaContentDelete)
}

//All
func ktaContentAll(c *gin.Context) {
	mdl := models.KtaContent{}
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
func ktaContentOne(c *gin.Context) {
	var mdl models.KtaContent
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
func ktaContentCreate(c *gin.Context) {
	var mdl models.KtaContent
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
func ktaContentUpdate(c *gin.Context) {
	var mdl models.KtaContent
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
func ktaContentDelete(c *gin.Context) {
	var mdl models.KtaContent
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
