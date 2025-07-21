package data

import (
	"encoding/csv"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

// LoadHeartData reads the heart disease data from a CSV file and returns a slice of HeartData structs.
func LoadHeartData(filePath string) ([]HeartData, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.LazyQuotes = true

	// Read header row
	_, err = reader.Read()
	if err != nil {
		return nil, err
	}

	var records []HeartData
	for {
		row, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		year, err := strconv.Atoi(row[4])
		if err != nil {
			log.Printf("Could not parse year: %v", err)
			year = 0
		}

		record := HeartData{
			Entity:                 row[1],
			Age:                    row[2],
			Cause:                  row[3],
			Year:                   year,
			PrevalenceCountBoth:    parseFloat(row[5]),
			DeathCountBoth:         parseFloat(row[6]),
			PrevalenceRateBoth:     parseFloat(row[7]),
			DeathRateBoth:          parseFloat(row[8]),
			PrevalencePercentBoth:  parseFloat(row[9]),
			DeathPercentBoth:       parseFloat(row[10]),
			PrevalenceCountFemale:  parseFloat(row[11]),
			DeathCountFemale:       parseFloat(row[12]),
			PrevalenceRateFemale:   parseFloat(row[13]),
			DeathRateFemale:        parseFloat(row[14]),
			PrevalencePercentFemale: parseFloat(row[15]),
			DeathPercentFemale:     parseFloat(row[16]),
			PrevalenceCountMale:    parseFloat(row[17]),
			DeathCountMale:         parseFloat(row[18]),
			PrevalenceRateMale:     parseFloat(row[19]),
			DeathRateMale:          parseFloat(row[20]),
			PrevalencePercentMale:  parseFloat(row[21]),
			DeathPercentMale:       parseFloat(row[22]),
			Code:                   row[23],
			GDPPC:                  parseFloat(row[24]),
			WBIncome:               row[25],
			CTUnits:                parseFloat(row[26]),
			ObesityPercent:         parseFloat(row[27]),
			Pacemaker1M:            parseFloat(row[28]),
			Population:             parseFloat(row[29]),
			Region:                 row[30],
			HTNCtrl:                parseFloat(row[31]),
			HighBP3079:             parseFloat(row[32]),
			HTNDiag:                parseFloat(row[33]),
			HTNRx3079:              parseFloat(row[34]),
		}
		records = append(records, record)
	}

	return records, nil
}

// LoadTrendsData reads the trends data from a CSV file and returns a slice of TrendsData structs.
func LoadTrendsData(filePath string) ([]TrendsData, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.LazyQuotes = true

	// Read header row
	_, err = reader.Read()
	if err != nil {
		return nil, err
	}

	var records []TrendsData
	for {
		row, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		year, err := strconv.Atoi(row[3])
		if err != nil {
			log.Printf("Could not parse year: %v", err)
			year = 0
		}

		isProjection, err := strconv.ParseBool(row[22])
		if err != nil {
			log.Printf("Could not parse is_projection: %v", err)
			isProjection = false
		}

		record := TrendsData{
			Cause:                   row[1],
			Age:                     row[2],
			Year:                    year,
			PrevalenceCountBoth:     parseFloat(row[4]),
			DeathCountBoth:          parseFloat(row[5]),
			PrevalenceRateBoth:      parseFloat(row[6]),
			DeathRateBoth:           parseFloat(row[7]),
			PrevalencePercentBoth:   parseFloat(row[8]),
			DeathPercentBoth:        parseFloat(row[9]),
			PrevalenceCountFemale:   parseFloat(row[10]),
			DeathCountFemale:        parseFloat(row[11]),
			PrevalenceRateFemale:    parseFloat(row[12]),
			DeathRateFemale:         parseFloat(row[13]),
			PrevalencePercentFemale: parseFloat(row[14]),
			DeathPercentFemale:      parseFloat(row[15]),
			PrevalenceCountMale:     parseFloat(row[16]),
			DeathCountMale:          parseFloat(row[17]),
			PrevalenceRateMale:      parseFloat(row[18]),
			DeathRateMale:           parseFloat(row[19]),
			PrevalencePercentMale:   parseFloat(row[20]),
			DeathPercentMale:        parseFloat(row[21]),
			IsProjection:            isProjection,
		}
		records = append(records, record)
	}

	return records, nil
}

func parseFloat(s string) *float64 {
	trimmed := strings.TrimSpace(s)
	if trimmed == "" {
		zero := 0.0
		return &zero
	}
	val, err := strconv.ParseFloat(trimmed, 64)
	if err != nil {
		log.Printf("Warning: could not parse '%s' as float, defaulting to 0.0", s)
		zero := 0.0
		return &zero
	}
	return &val
}
