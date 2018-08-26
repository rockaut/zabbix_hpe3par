package main

import (
	"os"

	"github.com/rockaut/zabbix_hpe3par/cli"
)

func main() {
	os.Exit(cli.Run(os.Args[1:]))
}
