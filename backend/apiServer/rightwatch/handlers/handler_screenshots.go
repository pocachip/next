package handlers

import (
	"rightwatch/models"
	"strconv"

	"github.com/gin-gonic/gin"
)

func init() {
	groupApi.GET("screenshots", screenshotsAll)
	groupApi.GET("screentshots/:id", screenshotsOne)
	groupApi.POST("screentshots", screenshotsCreate)
	groupApi.PATCH("screentshots", screenshotsUpdate)
	groupApi.DELETE("screentshots/:id", screenshotsDelete)
}

// All
func screenshotsAll(c *gin.Context) {
	mdl := models.Screenshots{}
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

// One
func screenshotsOne(c *gin.Context) {
	var mdl models.Screenshots

	//id, err := parseParamID(c)
	//if handleError(c, err) {
	//return
	//}

	mdl.UrlMd5 = "" //check for normal
	data, err := mdl.One()
	if handleError(c, err) {
		return
	}
	jsonData(c, data)
}

// Create
func screenshotsCreate(c *gin.Context) {
	var mdl models.Screenshots
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

// Update
func screenshotsUpdate(c *gin.Context) {
	var mdl models.Screenshots
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

// Delete
func screenshotsDelete(c *gin.Context) {
	var mdl models.Screenshots
	id, err := parseParamID(c)
	if handleError(c, err) {
		return
	}

	mdl.UrlMd5 = strconv.FormatUint(uint64(id), 10)
	err = mdl.Delete()
	if handleError(c, err) {
		return
	}
	jsonSuccess(c)
}
