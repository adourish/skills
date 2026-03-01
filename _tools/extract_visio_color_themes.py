"""
Extract Section 508 color themes from HRSA Visio Template

This script extracts the color themes and palettes from the Visio template
to ensure Mermaid diagrams align with the official HRSA Section 508 colors.

Requirements:
- Windows OS
- Microsoft Visio installed
- pywin32 package: pip install pywin32
"""

import win32com.client
import os
import json

def rgb_to_hex(rgb_value):
    """Convert Visio RGB integer to hex color code"""
    # Visio stores RGB as a single integer: RGB = R + (G * 256) + (B * 65536)
    r = rgb_value & 0xFF
    g = (rgb_value >> 8) & 0xFF
    b = (rgb_value >> 16) & 0xFF
    return f"#{r:02x}{g:02x}{b:02x}"

def extract_color_themes(visio_file_path, output_dir=None):
    """
    Extract color themes from Visio file
    
    Args:
        visio_file_path: Path to the .vsdx file
        output_dir: Directory to save results
    
    Returns:
        dict: Extracted color theme information
    """
    
    # Initialize Visio application
    print("Starting Visio application...")
    visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = False
    
    # Open the document
    print(f"Opening file: {visio_file_path}")
    doc = visio.Documents.Open(visio_file_path)
    
    color_data = {
        'file': os.path.basename(visio_file_path),
        'themes': [],
        'page_colors': [],
        'shape_colors': []
    }
    
    try:
        # Extract theme colors
        print("\nExtracting theme colors...")
        try:
            theme = doc.Theme
            if theme:
                theme_info = {
                    'name': theme.Name if hasattr(theme, 'Name') else 'Default',
                    'colors': []
                }
                
                # Try to get theme colors
                try:
                    theme_colors = theme.ThemeColors
                    for i in range(theme_colors.Count):
                        color = theme_colors(i + 1)
                        theme_info['colors'].append({
                            'index': i,
                            'rgb': color,
                            'hex': rgb_to_hex(color)
                        })
                except:
                    pass
                
                color_data['themes'].append(theme_info)
        except Exception as e:
            print(f"  Could not extract theme: {e}")
        
        # Extract colors from pages
        print(f"\nExtracting colors from {doc.Pages.Count} pages...")
        for page_idx in range(1, doc.Pages.Count + 1):
            page = doc.Pages(page_idx)
            page_info = {
                'name': page.Name,
                'background': None,
                'shape_fills': [],
                'shape_lines': [],
                'text_colors': []
            }
            
            print(f"  Page {page_idx}: {page.Name}")
            
            # Get page background color
            try:
                bg_color = page.PageSheet.CellsU("FillForegnd").ResultIU
                page_info['background'] = {
                    'rgb': int(bg_color),
                    'hex': rgb_to_hex(int(bg_color))
                }
            except:
                pass
            
            # Extract colors from shapes
            for shape_idx in range(1, min(page.Shapes.Count + 1, 51)):  # Limit to first 50 shapes
                try:
                    shape = page.Shapes(shape_idx)
                    
                    # Fill color
                    try:
                        fill_color = shape.CellsU("FillForegnd").ResultIU
                        fill_hex = rgb_to_hex(int(fill_color))
                        if fill_hex not in [c['hex'] for c in page_info['shape_fills']]:
                            page_info['shape_fills'].append({
                                'rgb': int(fill_color),
                                'hex': fill_hex,
                                'shape': shape.Name
                            })
                    except:
                        pass
                    
                    # Line color
                    try:
                        line_color = shape.CellsU("LineColor").ResultIU
                        line_hex = rgb_to_hex(int(line_color))
                        if line_hex not in [c['hex'] for c in page_info['shape_lines']]:
                            page_info['shape_lines'].append({
                                'rgb': int(line_color),
                                'hex': line_hex,
                                'shape': shape.Name
                            })
                    except:
                        pass
                    
                    # Text color
                    try:
                        text_color = shape.CellsU("Char.Color").ResultIU
                        text_hex = rgb_to_hex(int(text_color))
                        if text_hex not in [c['hex'] for c in page_info['text_colors']]:
                            page_info['text_colors'].append({
                                'rgb': int(text_color),
                                'hex': text_hex,
                                'shape': shape.Name
                            })
                    except:
                        pass
                    
                except Exception as e:
                    continue
            
            color_data['page_colors'].append(page_info)
        
        # Extract document colors
        print("\nExtracting document color palette...")
        try:
            colors = doc.Colors
            doc_colors = []
            for i in range(colors.Count):
                try:
                    color = colors(i)
                    doc_colors.append({
                        'index': i,
                        'rgb': color,
                        'hex': rgb_to_hex(color)
                    })
                except:
                    pass
            color_data['document_colors'] = doc_colors
        except Exception as e:
            print(f"  Could not extract document colors: {e}")
        
    finally:
        # Close document and quit Visio
        print("\nClosing Visio...")
        doc.Close()
        visio.Quit()
    
    # Save results
    if output_dir is None:
        output_dir = os.path.dirname(visio_file_path)
    
    output_file = os.path.join(output_dir, 'visio_color_themes.json')
    print(f"\nSaving results to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(color_data, f, indent=2, ensure_ascii=False)
    
    # Create summary report
    summary_file = os.path.join(output_dir, 'visio_color_themes_summary.md')
    print(f"Creating summary: {summary_file}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# HRSA Visio Template Color Theme Extraction\n\n")
        f.write(f"**Source File:** {color_data['file']}\n\n")
        
        # Unique colors summary
        all_colors = set()
        for page in color_data['page_colors']:
            for fill in page['shape_fills']:
                all_colors.add(fill['hex'])
            for line in page['shape_lines']:
                all_colors.add(line['hex'])
            for text in page['text_colors']:
                all_colors.add(text['hex'])
        
        f.write(f"## Summary\n\n")
        f.write(f"- **Pages Analyzed:** {len(color_data['page_colors'])}\n")
        f.write(f"- **Unique Colors Found:** {len(all_colors)}\n\n")
        
        f.write(f"## All Unique Colors\n\n")
        f.write(f"| Hex Code | RGB | Preview |\n")
        f.write(f"|----------|-----|--------|\n")
        for color_hex in sorted(all_colors):
            # Find RGB value
            rgb_val = None
            for page in color_data['page_colors']:
                for fill in page['shape_fills']:
                    if fill['hex'] == color_hex:
                        rgb_val = fill['rgb']
                        break
                if rgb_val:
                    break
            
            r = rgb_val & 0xFF if rgb_val else 0
            g = (rgb_val >> 8) & 0xFF if rgb_val else 0
            b = (rgb_val >> 16) & 0xFF if rgb_val else 0
            
            f.write(f"| `{color_hex}` | RGB({r}, {g}, {b}) | <span style='background-color:{color_hex};color:white;padding:2px 10px;'>{color_hex}</span> |\n")
        
        f.write(f"\n## Colors by Page\n\n")
        for page in color_data['page_colors']:
            f.write(f"### {page['name']}\n\n")
            
            if page['background']:
                f.write(f"**Background:** `{page['background']['hex']}`\n\n")
            
            if page['shape_fills']:
                f.write(f"**Fill Colors ({len(page['shape_fills'])}):**\n")
                for fill in page['shape_fills'][:10]:  # First 10
                    f.write(f"- `{fill['hex']}` - {fill['shape']}\n")
                if len(page['shape_fills']) > 10:
                    f.write(f"- *...and {len(page['shape_fills']) - 10} more*\n")
                f.write(f"\n")
            
            if page['shape_lines']:
                f.write(f"**Line Colors ({len(page['shape_lines'])}):**\n")
                for line in page['shape_lines'][:10]:
                    f.write(f"- `{line['hex']}` - {line['shape']}\n")
                if len(page['shape_lines']) > 10:
                    f.write(f"- *...and {len(page['shape_lines']) - 10} more*\n")
                f.write(f"\n")
            
            if page['text_colors']:
                f.write(f"**Text Colors ({len(page['text_colors'])}):**\n")
                for text in page['text_colors'][:10]:
                    f.write(f"- `{text['hex']}` - {text['shape']}\n")
                if len(page['text_colors']) > 10:
                    f.write(f"- *...and {len(page['text_colors']) - 10} more*\n")
                f.write(f"\n")
    
    print("\n✅ Extraction complete!")
    print(f"   - JSON data: {output_file}")
    print(f"   - Summary: {summary_file}")
    print(f"   - Unique colors found: {len(all_colors)}")
    
    return color_data


def main():
    """Main execution"""
    
    # Path to HRSA Visio template
    visio_file = r"G:\My Drive\HRSA Visio 508 Compliant Template V1.0.vsdx"
    
    # Check if file exists
    if not os.path.exists(visio_file):
        print(f"❌ Error: File not found: {visio_file}")
        return
    
    print("=" * 60)
    print("HRSA Visio Template Color Theme Extractor")
    print("=" * 60)
    
    try:
        color_data = extract_color_themes(visio_file)
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
