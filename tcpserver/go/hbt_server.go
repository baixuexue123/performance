package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"log"
	"net"
)


// dropCR drops a terminal \r from the data.
func dropCR(data []byte) []byte {
	if len(data) > 0 && data[len(data)-1] == '\r' {
		return data[0 : len(data)-1]
	}
	return data
}

func ScanCRLF(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}
	if i := bytes.Index(data, []byte{'\r', '\n'}); i >= 0 {
		// We have a full newline-terminated line.
		return i + 2, dropCR(data[0:i]), nil
	}
	// If we're at EOF, we have a final, non-terminated line. Return it.
	if atEOF {
		return len(data), dropCR(data), nil
	}
	// Request more data.
	return 0, nil, nil
}

var reply = []byte("pong\r\n")

func HbtHandler(c net.Conn) {
	peername := c.RemoteAddr().String()
	fmt.Println("New Connection from ", peername)
	defer c.Close()
	scanner := bufio.NewScanner(c)
	scanner.Split(ScanCRLF)
	for scanner.Scan() {
		msg := scanner.Text()
		if msg == "ping" {
			c.Write(reply)
		} else {
			fmt.Println("Connection: ", peername, "ERROR: ", msg)
			break
		}
	}
	fmt.Println("Connection: ", peername, "lost")
}

func main() {
	var host string
	var port string
	flag.StringVar(&host, "host", "127.0.0.1", "主机")
	flag.StringVar(&port, "port", "8888", "端口")
	flag.Parse()

	l, err := net.Listen("tcp", fmt.Sprintf("%s:%s", host, port))
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := l.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go HbtHandler(conn)
	}
}
