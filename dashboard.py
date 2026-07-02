import pandas as pd
import plotly.express as px

# Load your CSV file
df = pd.read_csv('results_enriched.csv')

# Process your data
status_counts = df['status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

country_counts = df['country'].value_counts().head(10).reset_index()
country_counts.columns = ['Country', 'Count']

as_counts = df['as_name'].dropna().value_counts().head(10).reset_index()
as_counts.columns = ['Organization', 'Count']

# Color schemes
colors = ['#00FFFF', '#BF00FF', '#FF0055', '#FFD700', '#00FF00']

# =============================================================================
# CHART 1: IP Status (Pie Chart)
# =============================================================================
fig1 = px.pie(status_counts, values='Count', names='Status', hole=0.4, 
              color_discrete_sequence=colors,
              title=' IP Status Distribution (Alive vs Dead)')
fig1.update_layout(
    height=600,
    paper_bgcolor='#0a0a0a',
    font=dict(color='white', size=14),
    title_font=dict(color='#00FFFF', size=24)
)
fig1.write_html('chart_1_ip_status.html')
print("✅ Created: chart_1_ip_status.html")

# =============================================================================
# CHART 2: Top Countries (Bar Chart)
# =============================================================================
fig2 = px.bar(country_counts, x='Country', y='Count', 
              color='Count',
              color_continuous_scale='blues',
              title='🌍 Top 10 Countries by IP Count')
fig2.update_layout(
    height=600,
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#1a1a2e',
    font=dict(color='white', size=12),
    title_font=dict(color='#00FFFF', size=24),
    xaxis=dict(color='white'),
    yaxis=dict(color='white')
)
fig2.write_html('chart_2_countries.html')
print("✅ Created: chart_2_countries.html")

# =============================================================================
# CHART 3: Top Organizations (Bar Chart)
# =============================================================================
fig3 = px.bar(as_counts, x='Organization', y='Count',
              color='Count',
              color_continuous_scale='magenta',
              title='🏢 Top 10 Organizations by IP Count')
fig3.update_layout(
    height=600,
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#1a1a2e',
    font=dict(color='white', size=12),
    title_font=dict(color='#BF00FF', size=24),
    xaxis=dict(color='white', tickangle=45),
    yaxis=dict(color='white')
)
fig3.write_html('chart_3_organizations.html')
print("✅ Created: chart_3_organizations.html")

print("\n🎉 All 3 charts created successfully!")
print("👉 Open each HTML file in your browser to view them separately")