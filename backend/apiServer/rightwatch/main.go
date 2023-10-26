package main

import (
	"github.com/spf13/viper"
	_ "rightwatch/config"
	"rightwatch/handlers"
	"rightwatch/tasks"
)

func main() {
	if viper.GetBool("app.enable_cron") {
		go tasks.RunTasks()
	}
	defer handlers.Close()
	handlers.ServerRun()
}
