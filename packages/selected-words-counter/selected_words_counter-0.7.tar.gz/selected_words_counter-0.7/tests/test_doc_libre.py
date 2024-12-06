import shutil
import subprocess
from glob import glob


def process_doc_with_libreoffice(file_path):
    """
    Extract text from a .doc file using LibreOffice and remove the generated .txt file.

    Args:
        file_path (str): Path to the .doc file.

    Returns:
        str: Extracted text from the .doc file.
    """
    try:
        # Define output directory and file name

        output_file = file_path.replace(".doc", "")

        # Set path to libre office.
        subprocess.run(
            "set PATH=%PATH%;C:/Program Files/LibreOffice/program", shell=True
        )

        # Convert .doc to .txt using LibreOffice
        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "txt",
                "--outdir",
                output_file,
                file_path,
            ],
            check=True,
        )

        print("Done converting")

        # Read and store the content of the generated .txt file
        with open(glob(output_file + "/*")[0], "r", encoding="utf-8") as txt_file:
            content = txt_file.read()

        # Remove the generated .txt file
        shutil.rmtree(output_file)

        return content
    except subprocess.CalledProcessError as e:
        print(f"LibreOffice conversion error: {e}")
        return None
    except FileNotFoundError:
        print("LibreOffice is not installed or not in PATH.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


print(
    process_doc_with_libreoffice(
        "E:/repos/selected_words_counter/tests/test_data/this_is_a_testament_to_testing.doc"
    )
)
