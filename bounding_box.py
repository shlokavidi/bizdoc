import pdfplumber
from typing import List, Dict, Tuple
from dataclasses import dataclass
import fitz  # PyMuPDF
from PIL import Image, ImageDraw
import os

@dataclass
class TextBox:
    text: str
    x0: float  # left
    x1: float  # right
    y0: float  # top
    y1: float  # bottom
    page_number: int
    box_number: int = 0  # Added box number field

def extract_text_boxes(pdf_path: str) -> List[TextBox]:
    """
    Extract text and their bounding box coordinates from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        List[TextBox]: List of TextBox objects containing text and coordinates
    """
    text_boxes = []
    box_counter = 1  # Initialize counter for box numbering
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Iterate through each page
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract words with their bounding boxes
                words = page.extract_words(
                    keep_blank_chars=True,
                    use_text_flow=True,
                    x_tolerance=3,
                    y_tolerance=3
                )
                
                # Process each word
                for word in words:
                    text_box = TextBox(
                        text=word['text'],
                        x0=word['x0'],
                        x1=word['x1'],
                        y0=word['top'],
                        y1=word['bottom'],
                        page_number=page_num,
                        box_number=box_counter  # Add box number
                    )
                    text_boxes.append(text_box)
                    box_counter += 1
                    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return []
        
    return text_boxes

def merge_adjacent_boxes(text_boxes: List[TextBox], 
                        x_tolerance: float = 5, 
                        y_tolerance: float = 2) -> List[TextBox]:
    """
    Merge adjacent text boxes that likely form a single line or paragraph.
    
    Args:
        text_boxes (List[TextBox]): List of individual text boxes
        x_tolerance (float): Maximum horizontal gap between boxes to merge
        y_tolerance (float): Maximum vertical gap between boxes to merge
        
    Returns:
        List[TextBox]: List of merged text boxes
    """
    if not text_boxes:
        return []
    
    # Sort boxes by page number, then y-coordinate, then x-coordinate
    sorted_boxes = sorted(
        text_boxes,
        key=lambda box: (box.page_number, box.y0, box.x0)
    )
    
    merged_boxes = []
    current_box = sorted_boxes[0]
    
    for next_box in sorted_boxes[1:]:
        # Check if boxes are on the same page and close enough
        same_page = current_box.page_number == next_box.page_number
        x_close = next_box.x0 - current_box.x1 <= x_tolerance
        y_close = abs(next_box.y0 - current_box.y0) <= y_tolerance
        
        if same_page and x_close and y_close:
            # Merge boxes
            current_box = TextBox(
                text=f"{current_box.text} {next_box.text}",
                x0=min(current_box.x0, next_box.x0),
                x1=max(current_box.x1, next_box.x1),
                y0=min(current_box.y0, next_box.y0),
                y1=max(current_box.y1, next_box.y1),
                page_number=current_box.page_number,
                box_number=current_box.box_number
            )
        else:
            merged_boxes.append(current_box)
            current_box = next_box
    
    merged_boxes.append(current_box)
    return merged_boxes

def draw_boxes_on_pdf(input_pdf: str, text_boxes: List[TextBox], output_pdf: str):
    """
    Create a new PDF with numbered bounding boxes drawn in bright green.
    
    Args:
        input_pdf (str): Path to the input PDF
        text_boxes (List[TextBox]): List of TextBox objects to draw
        output_pdf (str): Path where the new PDF will be saved
    """
    # Open the PDF
    doc = fitz.open(input_pdf)
    
    # Define colors (values must be between 0 and 1)
    BOX_COLOR = (0, 1, 0)  # Bright green (R=0, G=1, B=0)
    TEXT_COLOR = (0, 0, 0)  # Black
    
    # Group boxes by page
    boxes_by_page = {}
    for box in text_boxes:
        if box.page_number not in boxes_by_page:
            boxes_by_page[box.page_number] = []
        boxes_by_page[box.page_number].append(box)
    
    # Process each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        if page_num + 1 in boxes_by_page:
            for box in boxes_by_page[page_num + 1]:
                # Draw rectangle
                rect = fitz.Rect(box.x0, box.y0, box.x1, box.y1)
                page.draw_rect(rect, color=BOX_COLOR, width=1.5)
                
                # Add box number
                text_point = fitz.Point(box.x0, box.y0 - 5)  # Position above the box
                page.insert_text(
                    text_point,
                    str(box.box_number),
                    color=BOX_COLOR,
                    fontsize=8
                )
    
    # Save the modified PDF
    doc.save(output_pdf)
    doc.close()

def main(pdf_path: str):
    """
    Main function to demonstrate usage.
    """
    # Extract individual text boxes
    text_boxes = extract_text_boxes(pdf_path)
    
    # Merge adjacent text boxes into logical groups
    merged_boxes = merge_adjacent_boxes(text_boxes)
    
    # Create output filename
    output_pdf = os.path.splitext(pdf_path)[0] + "_with_boxes.pdf"
    
    # Draw boxes on new PDF
    draw_boxes_on_pdf(pdf_path, merged_boxes, output_pdf)
    
    # Print results
    for box in merged_boxes:
        print(f"\nBox #{box.box_number} - Page {box.page_number}")
        print(f"Text: {box.text}")
        print(f"Coordinates: ({box.x0}, {box.y0}) to ({box.x1}, {box.y1})")

    print(f"""\n=========\n \
Input PDF: {pdf_path} and Output files created in folder: {output_pdf} \
            \n=========""")

if __name__ == "__main__":
    # Example usage
    # pdf_path = "one_page_po.pdf"
    pdf_path="sample_pdf.pdf"
    main(pdf_path)