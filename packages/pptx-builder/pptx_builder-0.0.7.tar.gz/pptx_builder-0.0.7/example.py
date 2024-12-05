# Define your slides content list
import pandas as pd
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt

from src.pptx_builder.custom_presentation_builder import CustomPresentationBuilder

# Sample DataFrame
data = {
    'Column 1': ['A1', 'A2', 'A3'],
    'Column 2': ['B1', 'B2', 'B3'],
    'Column 3': ['C1', 'C2', 'C3'],
}
df1 = pd.DataFrame(data)
slides_content_list = [
    {
        'layout': 'TITLE_AND_CONTENT',
        'title': 'Using placeholders',
        'title_font': {
            'name': 'Calibri',
            'size': Pt(32),
            'bold': True,
            'color': RGBColor(0, 0, 128)  # Navy Blue
        },
        'title_alignment': PP_ALIGN.CENTER,  # Center align the title
        'text': 'This is the introductory slide of the presentation.',
        'body_font': {
            'name': 'Times New Roman',
            'size': Pt(18),
            'bold': False,
            'color': RGBColor(0, 0, 0)  # Black
        },
        'body_alignment': PP_ALIGN.LEFT,  # Left align the body text
    },

    {
        'title': 'Welcome to the Presentation',
        'title_font': {
            'name': 'Calibri',
            'size': Pt(32),
            'bold': True
        },
        'title_position': {
            'left_cm': 2,
            'top_cm': 1,
            'width_cm': 29.867,
            'height_cm': 3
        },
        'text': 'This is the introductory slide of the presentation.',
        'body_font': {
            'name': 'Times New Roman',
            'size': Pt(18),
            'bold': False
        },
        'body_position': {
            'left_cm': 2,
            'top_cm': 5,
            'width_cm': 29.867,
            'height_cm': 12
        },
        'grid': {
            'columns': 2,
            'rows': 2,
            'image_configs': [
                {'test_imgs/plot_slide_1.png': (11, 7.78)},
                {'test_imgs/plot_slide_2.png': (11, 7.78)},
                {'test_imgs/plot_slide_3.png': (11, 7.78)},
                {'test_imgs/plot_slide_4.png': (11, 7.78)},
            ],
            'position_cm': {'left_cm': 5.93, 'top_cm': 2.16},
            'size_cm': {'width_cm': 22, 'height_cm': 15.4},
        },
        'layout': 'TITLE_AND_CONTENT',
    },
    {
        'title': 'DataFrame Table Slide',
        'layout': 'TITLE_AND_CONTENT',
        'table': {
            'dataframe': df1,
            'position': {
                'left_mm': 20,
                'top_mm': 50,
                'width_mm': 240,
                'height_mm': 130
            },
            'header_font': {
                'name': 'ＭＳ Ｐゴシック (本文)',
                'bold': True
            },
            'cell_font': {
                'name': 'ＭＳ Ｐゴシック (本文)',
                'bold': False
            }
        }
    }
]

# Create an instance of the class
presentation = CustomPresentationBuilder(slides_content_list)

# Generate the presentation and save it to a file
presentation.create_presentation('output_presentation.pptx')
