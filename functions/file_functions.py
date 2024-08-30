import os
import PyPDF2

def read_file(path: str, show_line_numbers: bool = True) -> str:
    """
    Returns the contents of a file at path, with line numbers at the beginning of each line if show_line_numbers is True.

    PARAMETERS DESCRIPTION:
    path -> the path of the file to read
    show_line_numbers -> flag to return text with line numbers
    """
    with open(path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        if show_line_numbers:
            lines = [f"{i+1}: {line}" for i, line in enumerate(lines)]
        return ''.join(lines)


def write_file(path: str, text: str) -> None:
    """
    Writes to the file at path or creates a new file at path with text

    PARAMETERS DESCRIPTION:
    path -> the path of the file to overwrite or create
    text -> the text to write into the file
    """
    with open(path, 'w', encoding="utf-8") as file:
        file.write(text)


def insert_into_file(path: str, line_number: int, text: str) -> None:
    """
    Inserts text into a file at the specified line number

    PARAMETERS DESCRIPTION:
    path -> the path of the file to insert text into
    line_number -> the line number where the text should be inserted (1-indexed)
    text -> the text to insert into the file
    """
    try:
        with open(path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        
        lines.insert(line_number - 1, text + '\n')
        
        with open(path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        raise Exception(f"Error inserting text into file: {str(e)}")


def append_file(path: str, text: str) -> None:
    """
    Appends to the file at path with text

    PARAMETERS DESCRIPTION:
    path -> the path of the file to append text
    text -> the text to append to file
    """
    with open(path, 'a', encoding="utf-8") as file:
        file.write(text)


def modify_file(path: str, start_line_number: int, end_line_number: int, text: str) -> None:
    """
    Replaces the range of start_line_number and end_line_number with text

    PARAMETERS DESCRIPTION:
    path -> the path of the file to modify
    start_line_number -> starting from 1, beginning of range of text to be replaced (inclusive)
    end_line_number -> starting from 1, end of range of text to be replaced (inclusive)
    text -> text to replace the range of lines with
    """
    assert start_line_number <= end_line_number

    with open(path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    lines[start_line_number-1:end_line_number] = [text + '\n']

    with open(path, 'w', encoding="utf-8") as file:
        file.writelines(lines)


def list_files_and_dir(path: str, recursive: bool = False, max_results: int = 100) -> str:
    """
    Lists all files and directories within the path provided

    PARAMETERS DESCRIPTION:
    path -> the path of the folder to list files
    recursive -> function will list files and subdirectories of the files
    max_results -> limits the number of files and subdirectories listed so that there's no chance this will take forever
    """

    count = 0
    result = ""
    if os.path.exists(path) and os.path.isdir(path):
        if recursive:
            for root, dirs, files in os.walk(path):
                if count >= max_results:
                    break
                for name in files:
                    result += os.path.join(root, name) + "\n"
                    count += 1
                if not files:
                    result += os.path.join(root, '') + "\n"
                    count += 1
        else:
            for item in os.listdir(path):
                if count >= max_results:
                    break
                current_path = os.path.join(path, item)
                if os.path.isdir(current_path):
                    current_path = os.path.join(current_path, '') # Show that it is a folder to differentiate
                result += current_path + "\n"
                count += 1
        
        return result
    else:
        raise ValueError(f"Path {path} does not exist or is not a folder!")


def delete_file_or_dir(path: str) -> None:
    """
    Deletes a file or a directory and all its files at the provided path

    PARAMETERS DESCRIPTION:
    path -> the path of the file or directory to delete
    """
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                os.rmdir(path)
            else:
                raise ValueError("Path exists but is neither a file nor a directory.")
        else:
            raise FileNotFoundError(f"Path '{path}' does not exist.")
    except Exception as e:
        raise Exception(f"Error deleting file or directory: {str(e)}")


def read_pdf_to_text(pdf_path: str):
    """
    Deletes a file or a directory and all its files at the provided path

    PARAMETERS DESCRIPTION:
    pdf_path -> the path of the file or directory to delete
    """
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text
