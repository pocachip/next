package handlers

import (
	"rightwatch/models"
	"github.com/gin-gonic/gin"
)

func init() {
	groupApi.GET("crawler-job", crawlerJobAll)
	groupApi.GET("crawler-job/:id",  crawlerJobOne)
	groupApi.POST("crawler-job",  crawlerJobCreate)
	groupApi.PATCH("crawler-job",  crawlerJobUpdate)
	groupApi.DELETE("crawler-job/:id",  crawlerJobDelete)
}
//All
func crawlerJobAll(c *gin.Context) {
	mdl := models.CrawlerJob{}
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
func crawlerJobOne(c *gin.Context) {
	var mdl models.CrawlerJob
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
func crawlerJobCreate(c *gin.Context) {
	var mdl models.CrawlerJob
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
func crawlerJobUpdate(c *gin.Context) {
	var mdl models.CrawlerJob
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
func crawlerJobDelete(c *gin.Context) {
	var mdl models.CrawlerJob
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
