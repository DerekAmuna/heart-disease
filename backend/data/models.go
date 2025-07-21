package data

// HeartData represents a single row of the heart disease dataset.
type HeartData struct {
	Entity                 string   `json:"entity"`
	Age                    string   `json:"age"`
	Cause                  string   `json:"cause"`
	Year                   int      `json:"year"`
	PrevalenceCountBoth    *float64 `json:"valprevnumberboth,omitempty"`
	DeathCountBoth         *float64 `json:"valdeathsnumberboth,omitempty"`
	PrevalenceRateBoth     *float64 `json:"valprevrateboth,omitempty"`
	DeathRateBoth          *float64 `json:"valdeathsrateboth,omitempty"`
	PrevalencePercentBoth  *float64 `json:"valprevpercentboth,omitempty"`
	DeathPercentBoth       *float64 `json:"valdeathspercentboth,omitempty"`
	PrevalenceCountFemale  *float64 `json:"valprevnumberfemale,omitempty"`
	DeathCountFemale       *float64 `json:"valdeathsnumberfemale,omitempty"`
	PrevalenceRateFemale   *float64 `json:"valprevratefemale,omitempty"`
	DeathRateFemale        *float64 `json:"valdeathsratefemale,omitempty"`
	PrevalencePercentFemale *float64 `json:"valprevpercentfemale,omitempty"`
	DeathPercentFemale     *float64 `json:"valdeathspercentfemale,omitempty"`
	PrevalenceCountMale    *float64 `json:"valprevnumbermale,omitempty"`
	DeathCountMale         *float64 `json:"valdeathsnumbermale,omitempty"`
	PrevalenceRateMale     *float64 `json:"valprevratemale,omitempty"`
	DeathRateMale          *float64 `json:"valdeathsratemale,omitempty"`
	PrevalencePercentMale  *float64 `json:"valprevpercentmale,omitempty"`
	DeathPercentMale       *float64 `json:"valdeathspercentmale,omitempty"`
	Code                   string   `json:"code,omitempty"`
	GDPPC                  *float64 `json:"gdp_pc,omitempty"`
	WBIncome               string   `json:"wb_income,omitempty"`
	CTUnits                *float64 `json:"ct_units,omitempty"`
	ObesityPercent         *float64 `json:"obesity_percent,omitempty"`
	Pacemaker1M            *float64 `json:"pacemaker_1m,omitempty"`
	Population             *float64 `json:"population,omitempty"`
	Region                 string   `json:"region,omitempty"`
	HTNCtrl                *float64 `json:"t_htn_ctrl,omitempty"`
	HighBP3079             *float64 `json:"t_high_bp_30-79,omitempty"`
	HTNDiag                *float64 `json:"t_htn_diag,omitempty"`
	HTNRx3079              *float64 `json:"t_htn_rx_30-79,omitempty"`
}

// TrendsData represents a single row of the trends dataset.
type TrendsData struct {
	Cause                   string   `json:"cause"`
	Age                     string   `json:"age"`
	Year                    int      `json:"year"`
	PrevalenceCountBoth     *float64 `json:"valprevnumberboth,omitempty"`
	DeathCountBoth          *float64 `json:"valdeathsnumberboth,omitempty"`
	PrevalenceRateBoth      *float64 `json:"valprevrateboth,omitempty"`
	DeathRateBoth           *float64 `json:"valdeathsrateboth,omitempty"`
	PrevalencePercentBoth   *float64 `json:"valprevpercentboth,omitempty"`
	DeathPercentBoth        *float64 `json:"valdeathspercentboth,omitempty"`
	PrevalenceCountFemale   *float64 `json:"valprevnumberfemale,omitempty"`
	DeathCountFemale        *float64 `json:"valdeathsnumberfemale,omitempty"`
	PrevalenceRateFemale    *float64 `json:"valprevratefemale,omitempty"`
	DeathRateFemale         *float64 `json:"valdeathsratefemale,omitempty"`
	PrevalencePercentFemale *float64 `json:"valprevpercentfemale,omitempty"`
	DeathPercentFemale      *float64 `json:"valdeathspercentfemale,omitempty"`
	PrevalenceCountMale     *float64 `json:"valprevnumbermale,omitempty"`
	DeathCountMale          *float64 `json:"valdeathsnumbermale,omitempty"`
	PrevalenceRateMale      *float64 `json:"valprevratemale,omitempty"`
	DeathRateMale           *float64 `json:"valdeathsratemale,omitempty"`
	PrevalencePercentMale   *float64 `json:"valprevpercentmale,omitempty"`
	DeathPercentMale        *float64 `json:"valdeathspercentmale,omitempty"`
	IsProjection            bool     `json:"is_projection"`
}
