import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
print("Loading data... this might take a minute.")
df = pd.read_csv('results_enriched.csv')

# 2. Helper function to get Top N
def get_top_n(column_name, n=10):
    return df[column_name].value_counts().head(n)

# 3. Get the data
print("Processing data...")
status_data = get_top_n('status', n=5) 
country_data = get_top_n('country', n=10) 
as_data = get_top_n('as_name', n=10) 

print("Drawing transparent charts...")

# Function to draw a beautiful, clean bar chart WITH TRANSPARENT BACKGROUND
def draw_clean_bar(data, title, filename, colors=None):
    plt.figure(figsize=(10, 6), facecolor='none')  # Transparent figure
    ax = plt.gca()
    ax.set_facecolor('none')  # Transparent axes
    
    # If no colors are provided, use the default blue
    if colors is None:
        colors = ['#36A2EB'] * len(data)
            
    plt.barh(range(len(data)), data.values, color=colors, height=0.6)
    plt.gca().invert_yaxis() 
    plt.yticks(range(len(data)), data.index, fontsize=11, color='white')  # White text
    plt.xlabel('Count', fontsize=12, fontweight='bold', color='white')  # White text
    plt.title(title, fontsize=14, fontweight='bold', pad=15, color='white')  # White text
    plt.grid(axis='x', linestyle='--', alpha=0.3)  # Subtle grid
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', transparent=True)  # Transparent save
    plt.show()

# --- DRAW THE 3 CHARTS ---

# Status gets Green (#2ECC71) and Red (#E74C3C)
draw_clean_bar(status_data, 'Status Distribution', 'status_clean.png', colors=['#E74C3C', '#2ECC71'])

# Country and AS get the default blue
draw_clean_bar(country_data, 'Top 10 Countries', 'country_clean.png')
draw_clean_bar(as_data, 'Top 10 AS Names', 'as_clean.png')

print("Done! Check your folder for the transparent images.")