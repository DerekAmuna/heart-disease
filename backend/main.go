package main

import (
	"log"
	"net/http"
	"runtime"
	"time"
	"fmt"

	"heart-disease/backend/data"

	"github.com/gin-gonic/gin"
	"github.com/shirou/gopsutil/cpu"
)

func main() {
	heartData, err := data.LoadHeartData("../data/heart_processed.csv")
	if err != nil {
		log.Fatalf("Failed to load heart data: %v", err)
	}

	trendsData, err := data.LoadTrendsData("../data/trends.csv")
	if err != nil {
		log.Fatalf("Failed to load trends data: %v", err)
	}

	r := gin.Default()

	r.GET("/api/heart-data", func(c *gin.Context) {
		c.JSON(200, heartData)
	})

	r.GET("/api/trends-data", func(c *gin.Context) {
		c.JSON(200, trendsData)
	})

	// System stats endpoint
	r.GET("/api/system-stats", func(c *gin.Context) {
		var memStats runtime.MemStats
		runtime.ReadMemStats(&memStats)

		// Get CPU usage percentage
		cpuPercent, err := cpu.Percent(time.Second, false)
		var cpuUsage float64
		if err != nil || len(cpuPercent) == 0 {
			cpuUsage = 0.0
		} else {
			cpuUsage = cpuPercent[0]
		}

		stats := map[string]interface{}{
			"cpu": map[string]interface{}{
				"usage_percent": fmt.Sprintf("%.2f", cpuUsage),
				"core_count":    runtime.NumCPU(),
			},
			"memory": map[string]interface{}{
				"allocated_bytes":    memStats.Alloc,
				"allocated_mb":       fmt.Sprintf("%.2f",float64(memStats.Alloc) / 1024 / 1024),
				"total_allocated_mb": fmt.Sprintf("%.2f", float64(memStats.TotalAlloc)/1024/1024),
				"system_memory_mb":   fmt.Sprintf("%.2f", float64(memStats.Sys)/1024/1024),
				"heap_allocated_mb":  fmt.Sprintf("%.2f", float64(memStats.HeapAlloc)/1024/1024),
				"heap_system_mb":     fmt.Sprintf("%.2f", float64(memStats.HeapSys)/1024/1024),
				"heap_objects":       memStats.HeapObjects,
			},
			"gc": map[string]interface{}{
				"num_gc":         memStats.NumGC,
				"pause_total_ns": memStats.PauseTotalNs,
				"next_gc_mb":     fmt.Sprintf("%.2f", float64(memStats.NextGC)/1024/1024),
			},
			"runtime": map[string]interface{}{
				"goroutines": runtime.NumGoroutine(),
				"go_version": runtime.Version(),
			},
			"timestamp": time.Now().Unix(),
		}

		c.JSON(http.StatusOK, stats)
	})

	// Serve static files
	r.Static("/static", "./public")

	// Fallback to index.html for SPA routes
	r.NoRoute(func(c *gin.Context) {
		c.File("./public/index.html")
	})

	log.Println("Starting server on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}
