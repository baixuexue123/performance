package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

func main() {

	router := httprouter.New()

	router.GET("/", index)

	log.Println("Serving on 127.0.0.1:9001")
	log.Fatal(http.ListenAndServe("127.0.0.1:9001", router))
}

func index(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	fmt.Fprintf(w, "<p>Hello World</p>")
	log.Println(r.RemoteAddr, r.RequestURI)
}
