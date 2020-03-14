package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

type Res struct {
	URL        string
	StatusCode int
	Duration   int64
}

func httpGet(url string) Res {
	start := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		log.Println(err)
	}
	defer resp.Body.Close()
	return Res{URL: url, StatusCode: resp.StatusCode, Duration: time.Since(start).Milliseconds()}
}

func executor(urls []string) []Res {
	resChan := make(chan Res, len(urls))
	wg := sync.WaitGroup{}
	for _, url := range urls {
		wg.Add(1)
		go func(url string) {
			resChan <- httpGet(url)
			wg.Done()
		}(url)
	}
	wg.Wait()
	close(resChan)
	results := make([]Res, 0, len(urls))
	for res := range resChan {
		results = append(results, res)
	}
	return results
}

var urls = []string{
	"http://www.sohu.com",
	"http://www.sina.com",
	"http://www.qq.com/",
	"http://www.zhaopin.com/",
	"http://www.jd.com/",
	"http://www.zhibo8.cc/",
	"http://www.iqiyi.com/",
	"http://www.bootcss.com/",
	"http://www.redis.cn/",
	"http://cnodejs.org/",
	"http://bbs.tianya.cn/",
	"http://spark.apache.org/",
}

func main() {
	start := time.Now()

	results := executor(urls)

	total := int64(0)
	for _, r := range results {
		fmt.Println(r)
		total += r.Duration
	}
	fmt.Println(total)
	fmt.Println(time.Since(start).Milliseconds())
}
