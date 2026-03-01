"""
Export HRSA Visio Template icons as PNG images for visual documentation

This script exports each master shape from the Visio template as a PNG image
so they can be displayed in markdown documentation.

Requirements:
- Windows OS
- Microsoft Visio installed
- pywin32 package: pip install pywin32
"""

import win32com.client
import os
from pathlib import Path

def export_visio_icons_as_images(visio_file_path, output_dir):
    """
    Export all master shapes from Visio file as PNG images
    
    Args:
        visio_file_path: Path to the .vsdx file
        output_dir: Directory to save PNG images
    """
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize Visio application
    print("Starting Visio application...")
    visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = False
    
    # Open the document
    print(f"Opening file: {visio_file_path}")
    doc = visio.Documents.Open(visio_file_path)
    
    exported_count = 0
    
    try:
        # Create a temporary page for exporting
        temp_page = doc.Pages.Add()
        temp_page.Name = "TempExport"
        
        print(f"\nExporting {doc.Masters.Count} master shapes as PNG images...")
        
        for master_idx in range(1, doc.Masters.Count + 1):
            master = doc.Masters(master_idx)
            master_name = master.Name
            
            # Clean filename (remove invalid characters)
            safe_name = "".join(c for c in master_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            
            try:
                # Drop master onto temp page
                shape = temp_page.Drop(master, 2, 2)
                
                # Set consistent size for icons
                shape.Cells("Width").ResultIU = 1.0
                shape.Cells("Height").ResultIU = 1.0
                
                # Export as PNG
                output_file = os.path.join(output_dir, f"{safe_name}.png")
                
                # Select the shape
                visio.ActiveWindow.Select(shape, 2)  # 2 = visSelect
                
                # Export selection as PNG
                visio.ActiveWindow.Selection.Export(output_file)
                
                print(f"  [{master_idx}/{doc.Masters.Count}] Exported: {safe_name}.png")
                
                # Delete the shape
                shape.Delete()
                
                exported_count += 1
                
            except Exception as e:
                print(f"  [{master_idx}/{doc.Masters.Count}] Error exporting {master_name}: {e}")
        
        # Delete temp page
        temp_page.Delete(1)  # 1 = force delete
        
    finally:
        # Close document and quit Visio
        print("\nClosing Visio...")
        doc.Close()
        visio.Quit()
    
    print(f"\n✅ Export complete!")
    print(f"   Exported {exported_count} icons to: {output_dir}")
    
    return exported_count


def main():
    """Main execution"""
    
    # Paths
    visio_file = r"G:\My Drive\HRSA Visio 508 Compliant Template V1.0.vsdx"
    output_dir = r"G:\My Drive\06_Skills\documentation\hrsa_icons"
    
    # Check if file exists
    if not os.path.exists(visio_file):
        print(f"❌ Error: File not found: {visio_file}")
        return
    
    print("=" * 60)
    print("HRSA Visio Template Icon Exporter")
    print("=" * 60)
    
    try:
        count = export_visio_icons_as_images(visio_file, output_dir)
        print(f"\n✅ Successfully exported {count} icons!")
        
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
