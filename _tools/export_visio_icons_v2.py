"""
Export Section 508 Visio Template icons as PNG images - Version 2
Using alternative COM approach with better error handling

Requirements:
- Windows OS
- Microsoft Visio installed
- pywin32 package: pip install pywin32
"""

import win32com.client
import pythoncom
import os
import time
from pathlib import Path

def export_visio_icons_as_images(visio_file_path, output_dir):
    """
    Export all master shapes from Visio file as PNG images
    Using EarlyBound COM with proper initialization
    
    Args:
        visio_file_path: Path to the .vsdx file
        output_dir: Directory to save PNG images
    """
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize COM
    pythoncom.CoInitialize()
    
    try:
        # Initialize Visio application using DispatchEx for new instance
        print("Starting Visio application...")
        visio = win32com.client.DispatchEx("Visio.Application")
        
        # Give Visio time to initialize
        time.sleep(2)
        
        # Open the document
        print(f"Opening file: {visio_file_path}")
        
        # Use absolute path
        abs_path = os.path.abspath(visio_file_path)
        
        # Open document
        docs = visio.Documents
        doc = docs.Open(abs_path)
        
        print(f"Document opened successfully")
        print(f"Found {doc.Masters.Count} master shapes")
        
        exported_count = 0
        skipped_count = 0
        
        # Get existing files to skip duplicates
        existing_files = set(os.listdir(output_dir)) if os.path.exists(output_dir) else set()
        
        # Create a temporary page for exporting
        pages = doc.Pages
        temp_page = pages.Add()
        temp_page.Name = "TempExport"
        
        print(f"\nExporting icons as PNG images...")
        print(f"Output directory: {output_dir}")
        print(f"Already exported: {len(existing_files)} files")
        print("-" * 60)
        
        # Iterate through all masters
        for master_idx in range(1, doc.Masters.Count + 1):
            try:
                master = doc.Masters.Item(master_idx)
                master_name = master.Name
                
                # Clean filename (remove invalid characters)
                safe_name = "".join(c for c in master_name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
                safe_name = safe_name.replace(' ', '_')
                output_filename = f"{safe_name}.png"
                
                # Skip if already exported
                if output_filename in existing_files:
                    print(f"  [{master_idx}/{doc.Masters.Count}] Skipped (exists): {output_filename}")
                    skipped_count += 1
                    continue
                
                # Drop master onto temp page
                shape = temp_page.Drop(master, 2.0, 2.0)
                
                # Set consistent size for icons (1 inch x 1 inch)
                shape.CellsU("Width").FormulaU = "1 in"
                shape.CellsU("Height").FormulaU = "1 in"
                
                # Build output path
                output_file = os.path.join(output_dir, output_filename)
                
                # Select the shape
                window = visio.ActiveWindow
                window.Select(shape, 2)  # 2 = visSelect
                
                # Export selection as PNG
                selection = window.Selection
                selection.Export(output_file)
                
                print(f"  [{master_idx}/{doc.Masters.Count}] Exported: {output_filename}")
                
                # Delete the shape to clean up
                shape.Delete()
                
                exported_count += 1
                
                # Small delay to prevent overwhelming Visio
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  [{master_idx}/{doc.Masters.Count}] Error exporting {master_name}: {e}")
                continue
        
        # Delete temp page
        print("\nCleaning up...")
        temp_page.Delete(1)  # 1 = force delete
        
        # Close document
        doc.Close()
        
        print(f"\n{'='*60}")
        print(f"✅ Export complete!")
        print(f"   Newly exported: {exported_count} icons")
        print(f"   Already existed: {skipped_count} icons")
        print(f"   Total icons: {exported_count + skipped_count}")
        print(f"   Output directory: {output_dir}")
        print(f"{'='*60}")
        
        return exported_count
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 0
        
    finally:
        # Quit Visio
        try:
            visio.Quit()
        except:
            pass
        
        # Uninitialize COM
        pythoncom.CoUninitialize()


def main():
    """Main execution"""
    
    # Paths
    visio_file = r"G:\My Drive\Section 508 Visio 508 Compliant Template V1.0.vsdx"
    output_dir = r"G:\My Drive\06_Skills\documentation\Section 508_icons"
    
    # Check if file exists
    if not os.path.exists(visio_file):
        print(f"❌ Error: File not found: {visio_file}")
        print(f"   Please verify the Visio template location")
        return
    
    print("=" * 60)
    print("Section 508 Visio Template Icon Exporter v2.0")
    print("=" * 60)
    print()
    
    try:
        count = export_visio_icons_as_images(visio_file, output_dir)
        
        if count > 0:
            print(f"\n✅ Successfully exported {count} new icons!")
        else:
            print(f"\n⚠️ No new icons were exported")
            print(f"   Check if all icons are already in: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

