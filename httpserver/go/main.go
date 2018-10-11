package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/julienschmidt/httprouter"
)

func main() {

	router := httprouter.New()

	router.GET("/", index)

	log.Println("Serving on 127.0.0.1:9002")
	log.Fatal(http.ListenAndServe("127.0.0.1:9002", router))
}

func index(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	time.Sleep(time.Millisecond * 100)
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, "<p>Hello World</p>")
	log.Println(r.RemoteAddr, r.RequestURI)
}
