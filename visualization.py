import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns


def load_data(file_path):
    return pd.read_csv(file_path)


def preprocess_data(data):
    for col in ["m_high_bp", "ischemic_rate", "t_cvd_std", "t_htn_ctrl"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["death_per_capita"] = data["death_std"] / data["Population"]
    return data


def create_risk_factor_correlation_heatmap(data):
    risk_factors = data[["m_high_bp", "ischemic_rate", "t_cvd_std", "t_htn_ctrl"]].corr()
    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=risk_factors.values,
            x=risk_factors.columns,
            y=risk_factors.columns,
            colorscale="Viridis",
        )
    )
    heatmap_fig.update_layout(
        title="Risk Factor Correlation Heatmap",
        xaxis_title="Risk Factors",
        yaxis_title="Risk Factors",
    )
    return heatmap_fig


def create_hypertension_control_chart(data):
    htn_control_avg = data.groupby("region", as_index=False)["t_htn_ctrl"].mean().dropna()
    return px.bar(
        htn_control_avg,
        x="region",
        y="t_htn_ctrl",
        title="Average Hypertension Control Rates by Region",
        labels={"t_htn_ctrl": "Hypertension Control Rate (%)"},
    )


def create_population_normalized_death_chart(data):
    normalized_death_fig = px.scatter(
        df,
        x="Year",
        y="death_per_capita",
        color="Entity",
        title="Population Normalized Death Rates Over Time",
        labels={"death_per_capita": "Death Rate per Capita"},
    )
    normalized_death_fig.update_xaxes(range=[2000, 2021])
    return normalized_death_fig


def create_region_bar_chart(data):
    region_avg = (
        data.groupby("region", as_index=False)["death_std"]
        .mean()
        .sort_values("death_std", ascending=False)
    )
    return px.bar(
        region_avg,
        x="region",
        y="death_std",
        title="Average Age-Standardized Death Rates by Region",
        labels={"death_std": "Average Death Rate (per 100,000)", "region": "Region"},
        template="plotly_white",
    )


def create_correlation_matrix(data):
    risk_factors_inner = ["obesity%", "ischemic_rate", "rheumatic_rate", "pacemaker_1m"]
    correlation_matrix = data[risk_factors_inner].corr().round(2)
    return px.imshow(
        correlation_matrix,
        title="Risk Factor Correlation Matrix",
        labels={"color": "Correlation"},
        color_continuous_scale="RdBu",
        aspect="auto",
    )


def create_income_violin(data):
    return px.violin(
        data,
        x="WB_Income",
        y="death_std",
        title="Death Rate Distribution by Income Level",
        labels={"WB_Income": "World Bank Income Level", "death_std": "Death Rate (per 100,000)"},
        template="plotly_white",
        box=True,
    )


def create_obesity_trends(data):
    obesity_trends = data.groupby(["Year", "region"])["obesity%"].mean().reset_index()
    return px.line(
        obesity_trends,
        x="Year",
        y="obesity%",
        color="region",
        title="Obesity Trends Over Time by Region",
        labels={"obesity%": "Obesity Rate (%)", "Year": "Year"},
        template="plotly_white",
    )


def create_statin_scatter(data):
    return px.scatter(
        data,
        x="statin_avail",
        y="death_std",
        color="WB_Income",
        title="Statin Availability vs Death Rate by Income Level",
        labels={
            "statin_avail": "Statin Availability (%)",
            "death_std": "Death Rate (per 100,000)",
        },
        template="plotly_white",
    )


def create_cvd_prevalence(data):
    prev_by_income = data.groupby("WB_Income", as_index=False)["prev"].mean()
    return px.bar(
        prev_by_income,
        x="WB_Income",
        y="prev",
        title="CVD Prevalence by World Bank Income Group",
        labels={"prev": "CVD Prevalence (%)", "WB_Income": "Income Level"},
        color="WB_Income",
        template="plotly_white",
    )


def heart_disease_trend_by_gender(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="Year", y="m_deaths", data=df, label="Male", ci=None, color="blue")
    sns.lineplot(x="Year", y="f_deaths", data=df, label="Female", ci=None, color="pink")
    plt.title("Trend of Heart Disease Deaths by Gender Over Time")
    plt.ylabel("Total Deaths")
    plt.legend()
    plt.show()


def obesity_vs_cvd_deaths(df):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="obesity%", y="deaths", hue="region", data=df, alpha=0.7)
    plt.title("Obesity Prevalence vs. Total Cardiovascular Deaths")
    plt.show()


def top_cvd_death_rates(df):
    top_cvd_countries = df.groupby("Entity")["death_rate"].mean().nlargest(10)
    top_cvd_countries.plot(kind="bar", figsize=(10, 6), color="darkred")
    plt.title("Top 10 Countries with Highest CVD Death Rates")
    plt.ylabel("Death Rate per 100,000")
    plt.show()


if __name__ == "__main__":
    FILE_PATH = "data/heart_disease_data.csv"
    df = load_data(FILE_PATH)
    df = preprocess_data(df)

    figs = {
        "risk_factor_heatmap": create_risk_factor_correlation_heatmap(df),
        "hypertension_control": create_hypertension_control_chart(df),
        "population_normalized_death": create_population_normalized_death_chart(df),
        "region_bar": create_region_bar_chart(df),
        "correlation_matrix": create_correlation_matrix(df),
        "income_violin": create_income_violin(df),
        "obesity_trends": create_obesity_trends(df),
        "statin_scatter": create_statin_scatter(df),
        "cvd_prevalence": create_cvd_prevalence(df),
    }
    for name, fig in figs.items():
        fig.show()

    heart_disease_trend_by_gender(df)
    obesity_vs_cvd_deaths(df)
    top_cvd_death_rates(df)
