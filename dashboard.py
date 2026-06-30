import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# 1. Load your exact CSV file
df = pd.read_csv('results_enriched.csv')

# 2. Process your data
status_counts = df['status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

country_counts = df['country'].value_counts().head(5).reset_index()
country_counts.columns = ['Country', 'Count']

# Handle potential empty cells in as_name
as_counts = df['as_name'].dropna().value_counts().head(5).reset_index()
as_counts.columns = ['Organization', 'Count']

# 3. Create individual charts with Cyberpunk colors
colors = ['#00FFFF', '#BF00FF', '#FF0055', '#FFD700', '#00FF00']

fig_pie = px.pie(status_counts, values='Count', names='Status', hole=0.4, color_discrete_sequence=colors)

# FIXED: Using solid neon colors instead of gradients
fig_country = px.bar(country_counts, x='Country', y='Count', color_discrete_sequence=['#00FFFF'])
fig_asn = px.bar(as_counts, x='Organization', y='Count', color_discrete_sequence=['#BF00FF'])

# 4. Combine them into ONE dashboard
dashboard = make_subplots(
    rows=1, cols=3, 
    specs=[[{'type':'domain'}, {'type':'xy'}, {'type':'xy'}]],
    subplot_titles=('IP Status (Alive vs Dead)', 'Top 5 Countries', 'Top 5 Organizations')
)

# Add the charts to the dashboard
dashboard.add_trace(fig_pie.data[0], row=1, col=1)
dashboard.add_trace(fig_country.data[0], row=1, col=2)
dashboard.add_trace(fig_asn.data[0], row=1, col=3)

# 5. Make it look awesome (Dark Mode)
dashboard.update_layout(
    height=600,
    title_text="🌐 Global IP Address Analytics Dashboard",
    title_font_size=28,
    title_font_color='#00FFFF',
    paper_bgcolor='#0a0a0a', # Dark background
    plot_bgcolor='#1a1a2e',  # Slightly lighter panel background
    font_color='white',
    showlegend=False
)

# 6. Save it as a file you can just double-click!
dashboard.write_html('my_ip_dashboard.html')
print("✅ SUCCESS! Your dashboard is ready.")
print("👉 Look in your folder for a file named 'my_ip_dashboard.html' and double-click it!")