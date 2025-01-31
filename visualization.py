import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

FILE_PATH = "data/heart_disease_data.csv"
df = pd.read_csv(FILE_PATH)


#  Risk Factor Correlation Analysis
for col in ["m_high_bp", "ischemic_rate", "t_cvd_std", "t_htn_ctrl"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# calculate the correlation
risk_factors = df[["m_high_bp", "ischemic_rate", "t_cvd_std", "t_htn_ctrl"]].corr()
heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=risk_factors.values, x=risk_factors.columns, y=risk_factors.columns, colorscale="Viridis"
    )
)
heatmap_fig.update_layout(
    title="Risk Factor Correlation Heatmap", xaxis_title="Risk Factors", yaxis_title="Risk Factors"
)


heatmap_fig.show()

#  Hypertension Control Rates by Region
htn_control_avg = df.groupby("region", as_index=False)["t_htn_ctrl"].mean().dropna()
htn_control_fig = px.bar(
    htn_control_avg,
    x="region",
    y="t_htn_ctrl",
    title="Average Hypertension Control Rates by Region",
    labels={"t_htn_ctrl": "Hypertension Control Rate (%)"},
)

#  Population Normalized Death Rates
df["death_per_capita"] = df["death_std"] / df["Population"]
normalized_death_fig = px.scatter(
    df,
    x="Year",
    y="death_per_capita",
    color="Entity",
    title="Population Normalized Death Rates Over Time",
    labels={"death_per_capita": "Death Rate per Capita"},
)
normalized_death_fig.update_xaxes(range=[2000, 2021])

htn_control_fig.show()
normalized_death_fig.show()


# Region-wise Death Rates
def create_region_bar_chart(data):
    region_avg = (
        data.groupby("region", as_index=False)["death_std"]
        .mean()
        .sort_values("death_std", ascending=False)
    )
    region_bar_fig = px.bar(
        region_avg,
        x="region",
        y="death_std",
        title="Average Age-Standardized Death Rates by Region",
        labels={"death_std": "Average Death Rate (per 100,000)", "region": "Region"},
        template="plotly_white",
    )
    region_bar_fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    return region_bar_fig


# Risk Factor Correlation Matrix
def create_correlation_matrix(data):
    risk_factors_inner = ["obesity%", "ischemic_rate", "rheumatic_rate", "pacemaker_1m"]
    correlation_matrix = data[risk_factors_inner].corr().round(2)

    correlation_fig = px.imshow(
        correlation_matrix,
        title="Risk Factor Correlation Matrix",
        labels={"color": "Correlation"},
        color_continuous_scale="RdBu",
        aspect="auto",
    )
    correlation_fig.update_layout(xaxis_tickangle=-45)
    return correlation_fig


# Income Level Distribution
def create_income_violin(data):
    income_violin_fig = px.violin(
        data,
        x="WB_Income",
        y="death_std",
        title="Death Rate Distribution by Income Level",
        labels={"WB_Income": "World Bank Income Level", "death_std": "Death Rate (per 100,000)"},
        template="plotly_white",
        box=True,  # Add box plot inside violin
    )
    income_violin_fig.update_layout(xaxis_tickangle=-45)
    return income_violin_fig


# Obesity Trends
def create_obesity_trends(data):
    # Calculate mean obesity rates by year and region
    obesity_trends = data.groupby(["Year", "region"])["obesity%"].mean().reset_index()

    obesity_trends_fig = px.line(
        obesity_trends,
        x="Year",
        y="obesity%",
        color="region",
        title="Obesity Trends Over Time by Region",
        labels={"obesity%": "Obesity Rate (%)", "Year": "Year"},
        template="plotly_white",
    )
    obesity_trends_fig.update_layout(xaxis={"dtick": 1}, legend_title="Region")
    return obesity_trends_fig


# Statin Availability Analysis
def create_statin_scatter(data):
    statin_fig = px.scatter(
        data,
        x="statin_avail",
        y="death_std",
        color="WB_Income",
        title="Statin Availability vs Death Rate by Income Level",
        labels={
            "statin_avail": "Statin Availability (%)",
            "death_std": "Death Rate (per 100,000)",
            "WB_Income": "Income Level",
        },
        template="plotly_white",
    )
    statin_fig.update_layout(legend_title="Income Level")
    return statin_fig


# CVD Prevalence by Income
def create_cvd_prevalence(data):
    # Calculate mean prevalence by income group
    prev_by_income = data.groupby("WB_Income", as_index=False)["prev"].mean()

    cvd_prevalence_fig = px.bar(
        prev_by_income,
        x="WB_Income",
        y="prev",
        title="CVD Prevalence by World Bank Income Group",
        labels={"prev": "CVD Prevalence (%)", "WB_Income": "Income Level"},
        color="WB_Income",
        template="plotly_white",
    )
    cvd_prevalence_fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    return cvd_prevalence_fig


# Create all visualizations
figs = {
    "region_bar": create_region_bar_chart(df),
    "correlation_matrix": create_correlation_matrix(df),
    "income_violin": create_income_violin(df),
    "obesity_trends": create_obesity_trends(df),
    "statin_scatter": create_statin_scatter(df),
    "cvd_prevalence": create_cvd_prevalence(df),
}

# Show all figures
for name, fig in figs.items():
    fig.show()


def create_regional_death_rates_scatter(data):
    """Create scatter plot of death rates by region with gender comparison"""
    regional_death_fig = go.Figure()

    # Add female death rates
    regional_death_fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["f_death_rate"],
            name="Female",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )

    # Add male death rates
    fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["m_death_rate"],
            name="Male",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )

    regional_death_fig.update_layout(
        title="Regional CVD Death Rates by Gender",
        xaxis_title="Region",
        yaxis_title="Death Rate (per 100,000)",
        template="plotly_white",
        showlegend=True,
        xaxis_tickangle=-45,
    )

    # Add buttons to filter by gender
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {"args": [{"visible": [True, True]}], "label": "Both", "method": "restyle"},
                    {"args": [{"visible": [True, False]}], "label": "Female", "method": "restyle"},
                    {"args": [{"visible": [False, True]}], "label": "Male", "method": "restyle"},
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.1,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top",
            }
        ]
    )

    return regional_death_fig


def create_regional_cvd_rates_scatter(data):
    """Create scatter plot of standardized CVD rates by region"""
    cvd_fig = go.Figure()

    # Add female CVD rates
    cvd_fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["f_cvd_std"],
            name="Female",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )

    # Add male CVD rates
    cvd_fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["m_cvd_std"],
            name="Male",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )

    cvd_fig.update_layout(
        title="Regional Standardized CVD Rates by Gender",
        xaxis_title="Region",
        yaxis_title="Standardized CVD Rate",
        template="plotly_white",
        showlegend=True,
        xaxis_tickangle=-45,
    )

    # Add buttons to filter by gender
    cvd_fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {"args": [{"visible": [True, True]}], "label": "Both", "method": "restyle"},
                    {"args": [{"visible": [True, False]}], "label": "Female", "method": "restyle"},
                    {"args": [{"visible": [False, True]}], "label": "Male", "method": "restyle"},
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.1,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top",
            }
        ]
    )

    return cvd_fig


def create_regional_prevalence_scatter(data):
    """Create scatter plot of CVD prevalence by region"""
    prevalence_fig = go.Figure()

    # Add female prevalence
    prevalence_fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["f_prev%"],
            name="Female",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )

    # Add male prevalence
    prevalence_fig.add_trace(
        go.Scatter(
            x=data["region"],
            y=data["m_prev%"],
            name="Male",
            mode="markers",
            marker={"size": 12, "symbol": "square"},
        )
    )


# Updated usage example:
figs = {
    # "death_rate": create_death_rate_comparison(df),
    "regional_death_rates": create_regional_death_rates_scatter(df),
    "regional_cvd_rates": create_regional_cvd_rates_scatter(df),
}

for name, fig in figs.items():
    fig.show()


# Trend of Heart Disease Deaths by Gender Over Time
def heart_disease_trend_by_gender():

    plt.figure(figsize=(12, 6))
    sns.lineplot(x="Year", y="m_deaths", data=df, label="Male", ci=None, color="blue")
    sns.lineplot(x="Year", y="f_deaths", data=df, label="Female", ci=None, color="pink")
    plt.title("Trend of Heart Disease Deaths by Gender Over Time")
    plt.ylabel("Total Deaths")
    plt.legend()
    plt.show()


# Obesity Prevalence vs. Total Cardiovascular Deaths
def obesity_vs_cvd_deaths():

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="obesity%", y="deaths", hue="region", data=df, alpha=0.7)
    plt.title("Obesity Prevalence vs. Total Cardiovascular Deaths")
    plt.show()


def top_cvd_death_rates():
    top_cvd_countries = df.groupby("Entity")["death_rate"].mean().nlargest(10)
    top_cvd_countries.plot(kind="bar", figsize=(10, 6), color="darkred")
    plt.title("Top 10 Countries with Highest CVD Death Rates")
    plt.ylabel("Death Rate per 100,000")
    plt.show()
