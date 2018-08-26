package types

import "reflect"

type DynamicData struct {
}

func init() {
	t["DynamicData"] = reflect.TypeOf((*DynamicData)(nil)).Elem()
}

type ID struct {
	DynamicData

	Id string `xml:"id"`
}

func init() {
	t["ID"] = reflect.TypeOf((*ID)(nil)).Elem()
}
