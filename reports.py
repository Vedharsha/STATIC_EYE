from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
import os
from flask import current_app

def generate_report(analysis_results):
    # Create a new image with a white background
    img_width, img_height = 800, 1000
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)

    # Load fonts (you might need to adjust the font path)
    title_font = ImageFont.truetype("arial.ttf", 36)
    subtitle_font = ImageFont.truetype("arial.ttf", 24)
    body_font = ImageFont.truetype("arial.ttf", 16)

    # Add title
    draw.text((20, 20), "Static Analysis Report", font=title_font, fill='black')

    # Add analysis results
    y_offset = 100
    for analysis_type, results in analysis_results.items():
        draw.text((20, y_offset), f"{analysis_type.capitalize()} Analysis Results:", font=subtitle_font, fill='black')
        y_offset += 40

        for result in results[:5]:  # Limit to top 5 results
            draw.text((40, y_offset), f"- {result}", font=body_font, fill='black')
            y_offset += 30

        y_offset += 20

    # Generate and add a bar chart
    plt.figure(figsize=(7, 4))
    plt.bar(analysis_results.keys(), [len(v) for v in analysis_results.values()])
    plt.xlabel('Analysis Type')
    plt.ylabel('Number of Findings')
    plt.title('Analysis Results Summary')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = Image.open(buf)
    
    # Paste the chart onto the main image
    image.paste(chart, (50, y_offset))

    # Save the image in the static folder
    static_folder = os.path.join(current_app.root_path, 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    
    file_path = os.path.join(static_folder, 'static_analysis_report.png')
    image.save(file_path)

    return 'static_analysis_report.png'