import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
import main  # Assuming the script is named main.py

@pytest.fixture
def setup_test_environment():
    # Create temporary directories for testing
    os.makedirs("test_text", exist_ok=True)
    os.makedirs("test_pdf", exist_ok=True)
    os.makedirs("test_db", exist_ok=True)
    
    # Create a dummy text file
    with open("test_text/test.txt", "w") as f:
        f.write("This is a test document.")
    
    yield
    
    # Cleanup after tests
    shutil.rmtree("test_text")
    shutil.rmtree("test_pdf")
    shutil.rmtree("test_db")

@patch("main.pdf_to_txt")
@patch("main.TextLoader")
@patch("main.RecursiveCharacterTextSplitter")
@patch("main.OpenAIEmbeddings")
@patch("main.Chroma")
@patch("main.ChatOpenAI")
def test_main_script(mock_ChatOpenAI, mock_Chroma, mock_OpenAIEmbeddings, 
                     mock_RecursiveCharacterTextSplitter, mock_TextLoader, 
                     mock_pdf_to_txt, setup_test_environment):
    
    # Mock the necessary components
    mock_TextLoader.return_value.load.return_value = [MagicMock()]
    mock_RecursiveCharacterTextSplitter.return_value.split_documents.return_value = [MagicMock()]
    mock_Chroma.return_value.as_retriever.return_value.invoke.return_value = [MagicMock()]
    mock_ChatOpenAI.return_value.invoke.return_value = MagicMock(content="Test response")

    # Modify paths for testing
    main.current_dir = os.getcwd()
    main.files_path = os.path.join(main.current_dir, "test_text")
    main.input_path = os.path.join(main.current_dir, "test_pdf")
    main.file_path = os.path.join(main.files_path, "test.txt")
    main.persist_dir = os.path.join(main.current_dir, "test_db", "chroma_db_meta")
    main.persistent_directory = os.path.join(main.current_dir, "test_db", "chroma_db_with_metadata")

    # Run the main script
    with patch("builtins.print"):  # Suppress print statements
        main.main()  # Assuming you've wrapped your script in a main() function

    # Assert that the necessary functions were called
    mock_pdf_to_txt.assert_called_once()
    mock_TextLoader.assert_called()
    mock_RecursiveCharacterTextSplitter.assert_called_once()
    mock_OpenAIEmbeddings.assert_called()
    mock_Chroma.assert_called()
    mock_ChatOpenAI.assert_called()

@pytest.mark.parametrize("persistent_directory_exists", [True, False])
@patch("os.path.exists")
@patch("main.Chroma")
@patch("main.OpenAIEmbeddings")
def test_chroma_db_initialization(mock_OpenAIEmbeddings, mock_Chroma, mock_exists, 
                                  persistent_directory_exists, setup_test_environment):
    mock_exists.side_effect = lambda path: path == "test_text" or persistent_directory_exists

    main.persistent_directory = "test_db/chroma_db_with_metadata"
    main.files_path = "test_text"

    with patch("builtins.print"):  # Suppress print statements
        main.initialize_chroma_db()

    if not persistent_directory_exists:
        mock_Chroma.from_documents.assert_called_once()
    else:
        mock_Chroma.assert_called_once()

@patch("main.ChatOpenAI")
@patch("main.Chroma")
def test_query_processing(mock_Chroma, mock_ChatOpenAI, setup_test_environment):
    mock_Chroma.return_value.as_retriever.return_value.invoke.return_value = [
        MagicMock(page_content="Relevant content")
    ]
    mock_ChatOpenAI.return_value.invoke.return_value = MagicMock(content="Test response")

    with patch("builtins.print"):  # Suppress print statements
        response = main.process_query("Test query")

    assert response == "Test response"
    mock_ChatOpenAI.return_value.invoke.assert_called_once()

if __name__ == "__main__":
    pytest.main()