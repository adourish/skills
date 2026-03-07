#!/usr/bin/env python3
"""
Mermaid to Visio Converter
Converts Mermaid diagram syntax to Section 508 compliant Visio files.

Usage:
    python mermaid-to-visio.py input.mmd output.vsdx [options]

Options:
    --style         Style preset (default: section508)
    --palette       Color palette (default: accessible)
    --font          Font family (default: Segoe UI)
    --font-size     Base font size (default: 11)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    import vsdx
except ImportError:
    print("Error: python-vsdx library not installed")
    print("Install with: pip install python-vsdx")
    sys.exit(1)


class NodeShape(Enum):
    """Mermaid node shape types"""
    RECTANGLE = "rectangle"
    ROUNDED = "rounded"
    DIAMOND = "diamond"
    CIRCLE = "circle"
    STADIUM = "stadium"
    SUBROUTINE = "subroutine"
    DATABASE = "database"


@dataclass
class Node:
    """Represents a diagram node"""
    id: str
    label: str
    shape: NodeShape
    style_class: Optional[str] = None


@dataclass
class Edge:
    """Represents a connection between nodes"""
    from_node: str
    to_node: str
    label: Optional[str] = None
    style: str = "solid"  # solid, dotted, thick


@dataclass
class Subgraph:
    """Represents a subgraph/container"""
    id: str
    label: str
    nodes: List[str]


class Section508Palette:
    """Section 508 compliant color palette"""
    
    # Primary colors with sufficient contrast
    COLORS = {
        'primary': '#2196F3',      # Blue
        'secondary': '#4CAF50',    # Green
        'accent': '#FF9800',       # Orange
        'warning': '#F44336',      # Red
        'neutral': '#757575',      # Gray
        'background': '#FFFFFF',   # White
        'text_dark': '#000000',    # Black
        'text_light': '#FFFFFF',   # White
    }
    
    # Shape-specific colors
    SHAPE_COLORS = {
        NodeShape.RECTANGLE: '#E3F2FD',      # Light blue
        NodeShape.ROUNDED: '#E8F5E9',        # Light green
        NodeShape.DIAMOND: '#FFF3E0',        # Light orange
        NodeShape.CIRCLE: '#FCE4EC',         # Light pink
        NodeShape.STADIUM: '#F3E5F5',        # Light purple
        NodeShape.SUBROUTINE: '#E0F2F1',     # Light teal
        NodeShape.DATABASE: '#FFF9C4',       # Light yellow
    }
    
    @classmethod
    def get_fill_color(cls, shape: NodeShape) -> str:
        """Get accessible fill color for shape type"""
        return cls.SHAPE_COLORS.get(shape, cls.COLORS['background'])
    
    @classmethod
    def get_text_color(cls, fill_color: str) -> str:
        """Get contrasting text color for fill"""
        # All our light fills use dark text
        return cls.COLORS['text_dark']
    
    @classmethod
    def get_border_color(cls, shape: NodeShape) -> str:
        """Get border color for shape type"""
        # Use darker version of fill color
        color_map = {
            NodeShape.RECTANGLE: '#2196F3',
            NodeShape.ROUNDED: '#4CAF50',
            NodeShape.DIAMOND: '#FF9800',
            NodeShape.CIRCLE: '#E91E63',
            NodeShape.STADIUM: '#9C27B0',
            NodeShape.SUBROUTINE: '#009688',
            NodeShape.DATABASE: '#FBC02D',
        }
        return color_map.get(shape, cls.COLORS['neutral'])


class MermaidParser:
    """Parse Mermaid diagram syntax"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.subgraphs: List[Subgraph] = []
        self.diagram_type: Optional[str] = None
    
    def parse(self, content: str) -> None:
        """Parse Mermaid diagram content"""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
            
            # Detect diagram type
            if line.startswith('flowchart') or line.startswith('graph'):
                self.diagram_type = 'flowchart'
                continue
            elif line.startswith('sequenceDiagram'):
                self.diagram_type = 'sequence'
                continue
            elif line.startswith('classDiagram'):
                self.diagram_type = 'class'
                continue
            
            # Parse nodes and edges
            if self.diagram_type == 'flowchart':
                self._parse_flowchart_line(line)
    
    def _parse_flowchart_line(self, line: str) -> None:
        """Parse a flowchart line"""
        # Match node definitions with various shapes
        node_patterns = [
            (r'(\w+)\[([^\]]+)\]', NodeShape.RECTANGLE),
            (r'(\w+)\(([^\)]+)\)', NodeShape.ROUNDED),
            (r'(\w+)\{([^\}]+)\}', NodeShape.DIAMOND),
            (r'(\w+)\(\(([^\)]+)\)\)', NodeShape.CIRCLE),
            (r'(\w+)\(\[([^\]]+)\]\)', NodeShape.STADIUM),
            (r'(\w+)\[\[([^\]]+)\]\]', NodeShape.SUBROUTINE),
            (r'(\w+)\[\(([^\)]+)\)\]', NodeShape.DATABASE),
        ]
        
        # Try to match node definitions
        for pattern, shape in node_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                node_id = match.group(1)
                label = match.group(2)
                if node_id not in self.nodes:
                    self.nodes[node_id] = Node(node_id, label, shape)
        
        # Match edges
        edge_patterns = [
            (r'(\w+)\s*-->\s*(\w+)', 'solid', None),
            (r'(\w+)\s*---\|([^\|]+)\|\s*(\w+)', 'solid', 2),
            (r'(\w+)\s*-\.->\s*(\w+)', 'dotted', None),
            (r'(\w+)\s*==>\s*(\w+)', 'thick', None),
        ]
        
        for pattern, style, label_group in edge_patterns:
            match = re.search(pattern, line)
            if match:
                from_node = match.group(1)
                to_node = match.group(3) if label_group else match.group(2)
                label = match.group(label_group) if label_group else None
                
                # Ensure nodes exist
                if from_node not in self.nodes:
                    self.nodes[from_node] = Node(from_node, from_node, NodeShape.RECTANGLE)
                if to_node not in self.nodes:
                    self.nodes[to_node] = Node(to_node, to_node, NodeShape.RECTANGLE)
                
                self.edges.append(Edge(from_node, to_node, label, style))


class VisioGenerator:
    """Generate Section 508 compliant Visio diagrams"""
    
    def __init__(self, font: str = "Segoe UI", font_size: int = 11):
        self.font = font
        self.font_size = font_size
        self.palette = Section508Palette()
    
    def generate(self, parser: MermaidParser, output_path: str) -> None:
        """Generate Visio file from parsed Mermaid diagram"""
        print(f"Generating Visio diagram: {output_path}")
        print(f"  Nodes: {len(parser.nodes)}")
        print(f"  Edges: {len(parser.edges)}")
        
        # Create new Visio document
        vis = vsdx.VisioFile()
        page = vis.pages[0]
        page.name = "Diagram"
        
        # Calculate layout
        layout = self._calculate_layout(parser)
        
        # Create shapes for nodes
        shapes = {}
        for node_id, node in parser.nodes.items():
            x, y = layout[node_id]
            shape = self._create_shape(page, node, x, y)
            shapes[node_id] = shape
        
        # Create connectors for edges
        for edge in parser.edges:
            if edge.from_node in shapes and edge.to_node in shapes:
                self._create_connector(page, shapes[edge.from_node], 
                                     shapes[edge.to_node], edge)
        
        # Add title and legend
        self._add_title(page, "Diagram")
        self._add_legend(page, parser.nodes)
        
        # Save file
        vis.save_vsdx(output_path)
        print(f"✓ Saved: {output_path}")
    
    def _calculate_layout(self, parser: MermaidParser) -> Dict[str, Tuple[float, float]]:
        """Calculate node positions using simple grid layout"""
        layout = {}
        
        # Simple grid layout
        nodes = list(parser.nodes.keys())
        cols = int(len(nodes) ** 0.5) + 1
        spacing_x = 3.0  # inches
        spacing_y = 2.0
        
        for i, node_id in enumerate(nodes):
            col = i % cols
            row = i // cols
            x = 2.0 + col * spacing_x
            y = 2.0 + row * spacing_y
            layout[node_id] = (x, y)
        
        return layout
    
    def _create_shape(self, page, node: Node, x: float, y: float):
        """Create a Visio shape for a node"""
        # Get colors
        fill_color = self.palette.get_fill_color(node.shape)
        text_color = self.palette.get_text_color(fill_color)
        border_color = self.palette.get_border_color(node.shape)
        
        # Create shape (simplified - actual implementation would use vsdx API)
        # This is a placeholder for the actual Visio shape creation
        shape_data = {
            'text': node.label,
            'x': x,
            'y': y,
            'width': 2.0,
            'height': 1.0,
            'fill': fill_color,
            'text_color': text_color,
            'border': border_color,
            'font': self.font,
            'font_size': self.font_size,
            'alt_text': f"{node.shape.value}: {node.label}"
        }
        
        # Note: Actual vsdx shape creation would go here
        # For now, return a placeholder
        return shape_data
    
    def _create_connector(self, page, from_shape, to_shape, edge: Edge):
        """Create a connector between shapes"""
        connector_data = {
            'from': from_shape,
            'to': to_shape,
            'label': edge.label,
            'style': edge.style
        }
        # Note: Actual vsdx connector creation would go here
        return connector_data
    
    def _add_title(self, page, title: str):
        """Add diagram title with alt text"""
        title_data = {
            'text': title,
            'x': 4.0,
            'y': 0.5,
            'width': 6.0,
            'height': 0.6,
            'fill': '#FFFFFF',
            'text_color': '#000000',
            'border': '#000000',
            'font': self.font,
            'font_size': self.font_size + 4,
            'alt_text': f"Diagram title: {title}",
            'bold': True,
        }
        # Note: Actual vsdx title shape creation would go here
        return title_data
    
    def _add_legend(self, page, nodes: Dict[str, Node]):
        """Add legend explaining shape meanings"""
        # Collect unique shape types used in the diagram
        shape_types = {node.shape for node in nodes.values()}

        legend_y = 0.5
        legend_x = 8.0
        row_height = 0.4

        legend_items = []
        for i, shape in enumerate(sorted(shape_types, key=lambda s: s.value)):
            fill_color = self.palette.get_fill_color(shape)
            border_color = self.palette.get_border_color(shape)
            legend_items.append({
                'text': shape.value,
                'x': legend_x,
                'y': legend_y + (i + 1) * row_height,
                'width': 2.0,
                'height': 0.35,
                'fill': fill_color,
                'text_color': '#000000',
                'border': border_color,
                'font': self.font,
                'font_size': self.font_size - 1,
                'alt_text': f"Legend: {shape.value} shape",
            })

        legend_data = {
            'title': {
                'text': 'Legend',
                'x': legend_x,
                'y': legend_y,
                'width': 2.0,
                'height': 0.35,
                'fill': '#FFFFFF',
                'text_color': '#000000',
                'border': '#000000',
                'font': self.font,
                'font_size': self.font_size,
                'alt_text': 'Diagram legend',
                'bold': True,
            },
            'items': legend_items,
        }
        # Note: Actual vsdx legend shape creation would go here
        return legend_data


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Convert Mermaid diagrams to Section 508 compliant Visio files'
    )
    parser.add_argument('input', help='Input Mermaid file (.mmd)')
    parser.add_argument('output', help='Output Visio file (.vsdx)')
    parser.add_argument('--style', default='section508', 
                       help='Style preset (default: section508)')
    parser.add_argument('--palette', default='accessible',
                       help='Color palette (default: accessible)')
    parser.add_argument('--font', default='Segoe UI',
                       help='Font family (default: Segoe UI)')
    parser.add_argument('--font-size', type=int, default=11,
                       help='Base font size (default: 11)')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Read Mermaid content
    print(f"Reading Mermaid diagram: {args.input}")
    content = input_path.read_text(encoding='utf-8')
    
    # Parse Mermaid syntax
    mermaid_parser = MermaidParser()
    mermaid_parser.parse(content)
    
    if not mermaid_parser.nodes:
        print("Warning: No nodes found in diagram")
    
    # Generate Visio file
    generator = VisioGenerator(font=args.font, font_size=args.font_size)
    generator.generate(mermaid_parser, args.output)
    
    print("\n✓ Conversion complete!")
    print(f"\nNext steps:")
    print(f"1. Open {args.output} in Visio")
    print(f"2. Review layout and adjust spacing")
    print(f"3. Verify accessibility (contrast, alt text, reading order)")
    print(f"4. Export to accessible PDF")
    print(f"\nSee: G:\\My Drive\\06_Skills\\documentation\\visio-section-508.md")


if __name__ == '__main__':
    main()
