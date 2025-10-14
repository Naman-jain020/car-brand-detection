import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

def plot_top_3_brands(brand_counts):
    if not brand_counts:
        brands, counts = [], []
    else:
        top_3 = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        brands, counts = zip(*top_3)
    plt.figure(figsize=(5,4))
    plt.bar(brands, counts, color=['red','blue','green'])
    plt.title('Top 3 Detected Brands')
    plt.xlabel('Brand')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('static/brand_chart.png')
    plt.close()
