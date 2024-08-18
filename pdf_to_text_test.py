import pytest
import os
import shutil
from unittest.mock import patch, mock_open
from pdf_to_text import pdf_to_txt  # Replace 'your_module' with the actual module name

@pytest.fixture
def setup_folders():
    input_folder = 'test_input'
    output_folder = 'test_output'
    os.makedirs(input_folder, exist_ok=True)
    yield input_folder, output_folder
    shutil.rmtree(input_folder, ignore_errors=True)
    shutil.rmtree(output_folder, ignore_errors=True)

def create_dummy_pdf(folder, filename):
    with open(os.path.join(folder, filename), 'w') as f:
        f.write('Dummy PDF content')

@patch('pdf_to_text.PyPDFLoader')
def test_pdf_to_txt_converts_pdf(mock_PyPDFLoader, setup_folders):
    input_folder, output_folder = setup_folders
    create_dummy_pdf(input_folder, 'test.pdf')
    
    mock_loader = mock_PyPDFLoader.return_value
    mock_loader.load.return_value = [type('obj', (object,), {'page_content': 'Test content'})]

    pdf_to_txt(input_folder, output_folder)

    assert os.path.exists(os.path.join(output_folder, 'test.txt'))
    with open(os.path.join(output_folder, 'test.txt'), 'r') as f:
        assert f.read() == 'Test content'

def test_pdf_to_txt_creates_output_folder(setup_folders):
    input_folder, output_folder = setup_folders
    create_dummy_pdf(input_folder, 'test.pdf')

    pdf_to_txt(input_folder, output_folder)

    assert os.path.exists(output_folder)

def test_pdf_to_txt_skips_non_pdf_files(setup_folders):
    input_folder, output_folder = setup_folders
    with open(os.path.join(input_folder, 'test.txt'), 'w') as f:
        f.write('Not a PDF')

    pdf_to_txt(input_folder, output_folder)

    assert not os.listdir(output_folder)

@patch('pdf_to_text.PyPDFLoader')
def test_pdf_to_txt_handles_exception(mock_PyPDFLoader, setup_folders):
    input_folder, output_folder = setup_folders
    create_dummy_pdf(input_folder, 'test.pdf')
    
    mock_PyPDFLoader.side_effect = Exception('Test exception')

    with patch('builtins.print') as mock_print:
        pdf_to_txt(input_folder, output_folder)
        mock_print.assert_called_with('Error processing test.pdf: Test exception')

@patch('pdf_to_text.PyPDFLoader')
def test_pdf_to_txt_multiple_pages(mock_PyPDFLoader, setup_folders):
    input_folder, output_folder = setup_folders
    create_dummy_pdf(input_folder, 'test.pdf')
    
    mock_loader = mock_PyPDFLoader.return_value
    mock_loader.load.return_value = [
        type('obj', (object,), {'page_content': 'Page 1 content'}),
        type('obj', (object,), {'page_content': 'Page 2 content'})
    ]

    pdf_to_txt(input_folder, output_folder)

    assert os.path.exists(os.path.join(output_folder, 'test.txt'))
    with open(os.path.join(output_folder, 'test.txt'), 'r') as f:
        assert f.read() == 'Page 1 content\nPage 2 content'