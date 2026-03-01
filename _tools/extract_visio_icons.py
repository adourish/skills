"""
Extract icons and shapes from HRSA Visio 508 Compliant Template

This script extracts icon information from the HRSA Visio template including:
- Icon shapes and their properties
- Stencil information
- Master shapes
- Icon metadata and sources

Requirements:
- Windows OS
- Microsoft Visio installed
- pywin32 package: pip install pywin32
"""

import win32com.client
import os
import json
from pathlib import Path

def extract_visio_icons(visio_file_path, output_dir=None):
    """
    Extract icon information from a Visio file
    
    Args:
        visio_file_path: Path to the .vsdx file
        output_dir: Directory to save extracted information (default: same as input file)
    
    Returns:
        dict: Extracted icon information
    """
    
    # Initialize Visio application
    print("Starting Visio application...")
    visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = False  # Run in background
    
    # Open the document
    print(f"Opening file: {visio_file_path}")
    doc = visio.Documents.Open(visio_file_path)
    
    icon_data = {
        'file': os.path.basename(visio_file_path),
        'pages': [],
        'stencils': [],
        'masters': [],
        'icon_catalog': []
    }
    
    try:
        # Extract information from each page
        print(f"\nProcessing {doc.Pages.Count} pages...")
        for page_idx in range(1, doc.Pages.Count + 1):
            page = doc.Pages(page_idx)
            page_info = {
                'name': page.Name,
                'shapes': []
            }
            
            print(f"  Page {page_idx}: {page.Name}")
            
            # Extract shapes from page
            for shape_idx in range(1, page.Shapes.Count + 1):
                shape = page.Shapes(shape_idx)
                
                shape_info = {
                    'name': shape.Name,
                    'text': shape.Text if hasattr(shape, 'Text') else '',
                    'type': shape.Type,
                    'master': shape.Master.Name if shape.Master else None,
                    'width': shape.Cells('Width').ResultIU if hasattr(shape, 'Cells') else None,
                    'height': shape.Cells('Height').ResultIU if hasattr(shape, 'Cells') else None,
                }
                
                # Try to get hyperlink if exists
                try:
                    if shape.Hyperlinks.Count > 0:
                        shape_info['hyperlink'] = shape.Hyperlinks(1).Address
                except:
                    pass
                
                # Try to get data properties
                try:
                    if hasattr(shape, 'Data1'):
                        shape_info['data1'] = shape.Data1
                    if hasattr(shape, 'Data2'):
                        shape_info['data2'] = shape.Data2
                    if hasattr(shape, 'Data3'):
                        shape_info['data3'] = shape.Data3
                except:
                    pass
                
                page_info['shapes'].append(shape_info)
            
            icon_data['pages'].append(page_info)
        
        # Extract stencil information
        print(f"\nProcessing {doc.Masters.Count} master shapes...")
        for master_idx in range(1, doc.Masters.Count + 1):
            master = doc.Masters(master_idx)
            
            master_info = {
                'name': master.Name,
                'base_id': master.BaseID if hasattr(master, 'BaseID') else None,
                'unique_id': master.UniqueID if hasattr(master, 'UniqueID') else None,
                'icon_size': master.IconSize if hasattr(master, 'IconSize') else None,
            }
            
            # Try to get prompt/description
            try:
                master_info['prompt'] = master.Prompt
            except:
                pass
            
            icon_data['masters'].append(master_info)
            
            # Add to icon catalog if it looks like an icon
            if any(keyword in master.Name.lower() for keyword in ['icon', 'symbol', 'shape', 'graphic']):
                icon_data['icon_catalog'].append({
                    'name': master.Name,
                    'category': 'Unknown',  # Will need to categorize manually
                    'source': 'HRSA Visio Template',
                    'license': 'Check template documentation'
                })
        
        # Extract document stencils
        print(f"\nProcessing document stencils...")
        try:
            for stencil_idx in range(1, visio.Documents.Count + 1):
                stencil_doc = visio.Documents(stencil_idx)
                if stencil_doc.Type == 2:  # Stencil type
                    stencil_info = {
                        'name': stencil_doc.Name,
                        'path': stencil_doc.Path if hasattr(stencil_doc, 'Path') else None,
                        'masters_count': stencil_doc.Masters.Count
                    }
                    icon_data['stencils'].append(stencil_info)
        except Exception as e:
            print(f"  Error processing stencils: {e}")
        
    finally:
        # Close document and quit Visio
        print("\nClosing Visio...")
        doc.Close()
        visio.Quit()
    
    # Save results
    if output_dir is None:
        output_dir = os.path.dirname(visio_file_path)
    
    output_file = os.path.join(output_dir, 'visio_icons_extracted.json')
    print(f"\nSaving results to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(icon_data, f, indent=2, ensure_ascii=False)
    
    # Create summary report
    summary_file = os.path.join(output_dir, 'visio_icons_summary.md')
    print(f"Creating summary: {summary_file}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# HRSA Visio Template Icon Extraction Summary\n\n")
        f.write(f"**Source File:** {icon_data['file']}\n\n")
        f.write(f"## Statistics\n\n")
        f.write(f"- **Pages:** {len(icon_data['pages'])}\n")
        f.write(f"- **Master Shapes:** {len(icon_data['masters'])}\n")
        f.write(f"- **Stencils:** {len(icon_data['stencils'])}\n")
        f.write(f"- **Potential Icons:** {len(icon_data['icon_catalog'])}\n\n")
        
        f.write(f"## Pages\n\n")
        for page in icon_data['pages']:
            f.write(f"### {page['name']}\n")
            f.write(f"- Shapes: {len(page['shapes'])}\n\n")
        
        f.write(f"## Master Shapes\n\n")
        f.write(f"| Name | Base ID | Unique ID |\n")
        f.write(f"|------|---------|----------|\n")
        for master in icon_data['masters'][:50]:  # First 50
            f.write(f"| {master['name']} | {master.get('base_id', 'N/A')} | {master.get('unique_id', 'N/A')} |\n")
        
        if len(icon_data['masters']) > 50:
            f.write(f"\n*...and {len(icon_data['masters']) - 50} more*\n")
        
        f.write(f"\n## Icon Catalog\n\n")
        if icon_data['icon_catalog']:
            f.write(f"| Icon Name | Category | Source | License |\n")
            f.write(f"|-----------|----------|--------|--------|\n")
            for icon in icon_data['icon_catalog']:
                f.write(f"| {icon['name']} | {icon['category']} | {icon['source']} | {icon['license']} |\n")
        else:
            f.write(f"*No icons identified. Check masters list above.*\n")
        
        f.write(f"\n## Next Steps\n\n")
        f.write(f"1. Review `visio_icons_extracted.json` for complete data\n")
        f.write(f"2. Categorize icons in the icon catalog\n")
        f.write(f"3. Verify licensing for each icon source\n")
        f.write(f"4. Add proper attribution if required\n")
        f.write(f"5. Create skill documentation for icon usage\n")
    
    print("\n✅ Extraction complete!")
    print(f"   - JSON data: {output_file}")
    print(f"   - Summary: {summary_file}")
    
    return icon_data


def main():
    """Main execution"""
    
    # Path to HRSA Visio template
    visio_file = r"G:\My Drive\HRSA Visio 508 Compliant Template V1.0.vsdx"
    
    # Check if file exists
    if not os.path.exists(visio_file):
        print(f"❌ Error: File not found: {visio_file}")
        print("\nPlease update the file path in the script.")
        return
    
    # Extract icons
    print("=" * 60)
    print("HRSA Visio Template Icon Extractor")
    print("=" * 60)
    
    try:
        icon_data = extract_visio_icons(visio_file)
        
        print("\n" + "=" * 60)
        print("Summary:")
        print("=" * 60)
        print(f"Pages extracted: {len(icon_data['pages'])}")
        print(f"Master shapes: {len(icon_data['masters'])}")
        print(f"Stencils: {len(icon_data['stencils'])}")
        print(f"Potential icons: {len(icon_data['icon_catalog'])}")
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
