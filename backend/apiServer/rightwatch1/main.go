package main

import (
	_ "rightwatch1/config"
	"rightwatch1/handlers"
	"rightwatch1/tasks"
	"github.com/spf13/viper"
)

func main() {
	if viper.GetBool("app.enable_cron") {
		go tasks.RunTasks()
	}
	defer handlers.Close()
	handlers.ServerRun()
}
