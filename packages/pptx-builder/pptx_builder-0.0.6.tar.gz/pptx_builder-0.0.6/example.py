# Define your slides content list
import pandas as pd

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
        'title': '1,2,3,4,5',
        'text': 'This slide contains a grid of images.',
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
