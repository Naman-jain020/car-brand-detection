"""
Visualization module for creating brand distribution charts
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server deployment
import os

def create_brand_chart(brand_counts, output_path='static/brand_chart.png'):
    """
    Create a bar chart showing car brand distribution
    
    Args:
        brand_counts: Dictionary mapping brand names to counts
        output_path: Path where the chart image will be saved
    """
    if not brand_counts:
        print("No brand data to visualize")
        return
    
    # Sort brands by count (descending)
    sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
    brands = [item[0] for item in sorted_brands]
    counts = [item[1] for item in sorted_brands]
    
    # Create figure and axis
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(brands, counts, color='#667eea', edgecolor='#764ba2', linewidth=2)
    
    # Customize the chart
    plt.xlabel('Car Brand', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Detections', fontsize=14, fontweight='bold')
    plt.title('Car Brand Detection Results', fontsize=16, fontweight='bold', pad=20)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Rotate x-axis labels if many brands
    if len(brands) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the chart
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Chart saved to: {output_path}")


def create_pie_chart(brand_counts, output_path='static/brand_pie_chart.png'):
    """
    Alternative: Create a pie chart showing brand distribution
    """
    if not brand_counts:
        return
    
    sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
    brands = [item[0] for item in sorted_brands]
    counts = [item[1] for item in sorted_brands]
    
    plt.figure(figsize=(10, 8))
    
    colors = plt.cm.Set3(range(len(brands)))
    
    plt.pie(counts, labels=brands, autopct='%1.1f%%', startangle=90,
            colors=colors, textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    plt.title('Car Brand Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Pie chart saved to: {output_path}")


if __name__ == "__main__":
    # Test the visualization
    test_data = {
        'Toyota': 15,
        'Honda': 12,
        'BMW': 10,
        'Ford': 8,
        'Mercedes': 5
    }
    
    create_brand_chart(test_data, '../static/test_chart.png')
    print("Test chart created successfully!")
