import pytest
from unittest.mock import patch, mock_open
from despensa.interfaces.logger import Logger  
import os

import definitions as d

# Test del método info
@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_logger_info(mock_makedirs, mock_file):
    logger = Logger(log_file='test.log')

    logger.info("Test info message")
    mock_makedirs.assert_called_once_with(d.LOGS_DIR)
    mock_file.assert_called_once_with(os.path.join(d.LOGS_DIR, 'test.log'), 'a')
    handle = mock_file()
    handle.write.assert_called_once()
    written_content = handle.write.call_args[0][0]
    
    assert "[INFO]" in written_content
    assert "Test info message" in written_content

# Test del método warning
@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_logger_warning(mock_makedirs, mock_file):
    logger = Logger(log_file='test.log')

    logger.warning("Test warning message")
    handle = mock_file()
    handle.write.assert_called_once()
    written_content = handle.write.call_args[0][0]
    assert "[WARNING]" in written_content
    assert "Test warning message" in written_content

# Test del método error
@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_logger_error(mock_makedirs, mock_file):
    logger = Logger(log_file='test.log')

    # Simulamos una llamada al método error
    logger.error("Test error message")

    # Verificamos que el archivo se abrió y se escribió correctamente
    handle = mock_file()
    handle.write.assert_called_once()

    # Verificamos que el mensaje contiene el nivel de log correcto
    written_content = handle.write.call_args[0][0]
    assert "[ERROR]" in written_content
    assert "Test error message" in written_content
