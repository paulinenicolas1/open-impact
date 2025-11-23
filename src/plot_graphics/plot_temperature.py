from plotly import express as px
import pandas as pd
from plotly.graph_objs._figure import Figure


def plot_temperature(df: pd.DataFrame,
                     year_column: str = 'year',
                     temperature_column: str = 'temperature',
                     title: str = "Température moyenne annuelle (°C)") -> Figure:
    fig = px.line(
        df,
        x=year_column,
        y=temperature_column,
        markers=True,
        title=title,
    )

    # 3) Personnalisation du graphe
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate="<b>%{x}</b><br>Température: %{y} °C<extra></extra>",
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Mois",
        yaxis_title="Température (°C)",
        font=dict(family="system-ui, -apple-system, BlinkMacSystemFont, sans-serif", size=14),
        title=dict(x=0.5, xanchor="center"),  # centrer le titre
        margin=dict(l=40, r=40, t=60, b=40),
    )

    # Optionnel : zones de couleur pour les saisons
    fig.add_vrect(x0="Déc", x1="Fév", fillcolor="lightblue", opacity=0.15, layer="below", line_width=0)
    fig.add_vrect(x0="Juin", x1="Août", fillcolor="orange", opacity=0.10, layer="below", line_width=0)
    return fig
