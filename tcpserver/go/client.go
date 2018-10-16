package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"log"
	"net"
	"sync"
	"time"
)

var TOTAL []time.Duration
var MAX []time.Duration
var AVG []time.Duration
var mu sync.Mutex

func ScanCRLF(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}
	if i := bytes.Index(data, []byte{'\r', '\n'}); i >= 0 {
		// We have a full newline-terminated line.
		return i + 2, data[0:i], nil
	}
	// If we're at EOF, we have a final, non-terminated line. Return it.
	if atEOF {
		return len(data), data, nil
	}
	// Request more data.
	return 0, nil, nil
}

func MaxMinAvg(s []time.Duration) (max, min, avg time.Duration) {
	if len(s) == 0 {
		return
	}
	min = s[0]
	var sum time.Duration
	for _, v := range s {
		if v > max {
			max = v
		}
		if v < min {
			min = v
		}
		sum += v
	}
	avg = sum / time.Duration(len(s))
	return
}

func Client(addr string, cnt, n int, wg *sync.WaitGroup) {
	name := fmt.Sprintf("Client - %d", n)
	defer wg.Done()

	conn, err := net.Dial("tcp", addr)
	if err != nil {
		log.Println(err)
		return
	}
	defer conn.Close()

	scanner := bufio.NewScanner(conn)
	scanner.Split(ScanCRLF)

	var elapsed []time.Duration
	start := time.Now()
	for i := 0; i < cnt; i++ {
		st := time.Now()
		_, err := conn.Write([]byte("ping\r\n"))
		if err != nil {
			fmt.Println(err)
			break
		}
		if scanner.Scan() {
			msg := scanner.Text()
			if msg != "pong" {
				fmt.Println(name, "ERROR: ", msg)
				break
			}
		} else {
			break
		}
		elapsed = append(elapsed, time.Since(st))
		time.Sleep(1 * time.Second)
	}

	total := time.Since(start)
	max, _, avg := MaxMinAvg(elapsed)
	mu.Lock()
	TOTAL = append(TOTAL, total)
	MAX = append(MAX, max)
	AVG = append(AVG, avg)
	mu.Unlock()
}

func main() {
	var host, port string
	var num, cnt int
	flag.StringVar(&host, "host", "127.0.0.1", "主机")
	flag.StringVar(&port, "port", "8888", "端口")
	flag.IntVar(&num, "num", 1000, "客户端数量")
	flag.IntVar(&cnt, "count", 10, "ping/pong次数, 一秒一次")
	flag.Parse()

	addr := fmt.Sprintf("%s:%s", host, port)
	wg := sync.WaitGroup{}
	start := time.Now()
	for i := 0; i < num; i++ {
		wg.Add(1)
		go Client(addr, cnt, i, &wg)
	}
	wg.Wait()

	fmt.Println("Clients: ", num)
	fmt.Println("======================", time.Since(start), "======================")
	fmt.Println("********************** TOTAL **********************")
	fmt.Println(TOTAL)
	max, min, avg := MaxMinAvg(TOTAL)
	fmt.Printf("MAX: %.3f AVG: %.3f MIN: %.3f\n", max.Seconds(), avg.Seconds(), min.Seconds())
	fmt.Println("********************** MAX **********************")
	max, min, avg = MaxMinAvg(MAX)
	fmt.Printf("MAX: %.3f AVG: %.3f MIN: %.3f\n", max.Seconds(), avg.Seconds(), min.Seconds())
	fmt.Println("********************** AVG **********************")
	max, min, avg = MaxMinAvg(AVG)
	fmt.Printf("MAX: %.3f AVG: %.3f MIN: %.3f\n", max.Seconds(), avg.Seconds(), min.Seconds())
}
