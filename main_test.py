import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
import main

@pytest.fixture
def setup_test_environment():
    # Create temporary directories for testing
    current_dir = os.getcwd()
    os.makedirs(os.path.join(current_dir, "test_text"), exist_ok=True)
    os.makedirs(os.path.join(current_dir, "test_pdf"), exist_ok=True)
    os.makedirs(os.path.join(current_dir, "test_db"), exist_ok=True)
    
    # Create a dummy text file
    with open(os.path.join(current_dir, "test_text", "test.txt"), "w") as f:
        f.write("This is a test document.")
    
    yield
    
    # Cleanup after tests
    shutil.rmtree(os.path.join(current_dir, "test_text"))
    shutil.rmtree(os.path.join(current_dir, "test_pdf"))
    shutil.rmtree(os.path.join(current_dir, "test_db"))

@patch("main.pdf_to_txt")
@patch("main.TextLoader")
@patch("main.RecursiveCharacterTextSplitter")
@patch("main.OpenAIEmbeddings")
@patch("main.Chroma")
@patch("main.ChatOpenAI")
@patch("os.path.exists")
def test_main_script(mock_exists, mock_ChatOpenAI, mock_Chroma, mock_OpenAIEmbeddings, 
                     mock_RecursiveCharacterTextSplitter, mock_TextLoader, 
                     mock_pdf_to_txt, setup_test_environment):
    
    # Mock os.path.exists to always return True
    mock_exists.return_value = True

    # Mock the necessary components
    mock_document = MagicMock()
    mock_document.page_content = "This is a test document content."
    mock_TextLoader.return_value.load.return_value = [mock_document]
    mock_RecursiveCharacterTextSplitter.return_value.split_documents.return_value = [mock_document]
    mock_Chroma.return_value.as_retriever.return_value.invoke.return_value = [mock_document]
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
        main.main()

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
@patch("main.TextLoader")
@patch("main.CharacterTextSplitter")
def test_initialize_chroma_db(mock_CharacterTextSplitter, mock_TextLoader, 
                              mock_OpenAIEmbeddings, mock_Chroma, mock_exists, 
                              persistent_directory_exists, setup_test_environment):
    mock_exists.side_effect = lambda path: path == os.path.join(os.getcwd(), "test_text") or persistent_directory_exists

    main.persistent_directory = os.path.join(os.getcwd(), "test_db", "chroma_db_with_metadata")
    main.files_path = os.path.join(os.getcwd(), "test_text")

    mock_document = MagicMock()
    mock_document.page_content = "This is a test document content."
    mock_TextLoader.return_value.load.return_value = [mock_document]
    mock_CharacterTextSplitter.return_value.split_documents.return_value = [mock_document]

    with patch("builtins.print"):  # Suppress print statements
        main.initialize_chroma_db()

    mock_OpenAIEmbeddings.assert_called_once()
    if not persistent_directory_exists:
        mock_Chroma.from_documents.assert_called_once()
    else:
        mock_Chroma.assert_called_once()

@patch("main.ChatOpenAI")
@patch("main.Chroma")
@patch("main.initialize_chroma_db")
def test_process_query(mock_initialize_chroma_db, mock_Chroma, mock_ChatOpenAI, setup_test_environment):
    mock_document = MagicMock()
    mock_document.page_content = "This is relevant content."
    mock_Chroma.return_value.as_retriever.return_value.invoke.return_value = [mock_document]
    mock_ChatOpenAI.return_value.invoke.return_value = MagicMock(content="Test response")
    mock_initialize_chroma_db.return_value = mock_Chroma.return_value

    with patch("builtins.print"):  # Suppress print statements
        response = main.process_query("Test query")

    assert response == "Test response"
    mock_initialize_chroma_db.assert_called_once()
    mock_ChatOpenAI.return_value.invoke.assert_called_once()

if __name__ == "__main__":
    pytest.main()