# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['langcodes[data]>=3.3.0,<4.0.0',
 'lingua-language-detector>=1.3.2,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'rich>=13.4.2,<14.0.0',
 'sh>=2.0.4,<3.0.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['pdf-language-detector = src.cli:app',
                     'pld = src.cli:app']}

setup_kwargs = {
    'name': 'pdf-language-detector',
    'version': '0.0.8',
    'description': 'A python script to iterate over a list of PDF in a directory and try to guess their language with Tesseract OCR.',
    'long_description': "# PLD (PDF Language Detector)\n\nPLD is a Python program that analyzes PDF files, extracts images, processes them using Optical Character Recognition (OCR), and detects the dominant language of the text. It provides language detection information in JSON format and calculates the average confidence coefficient for each language.\n\n## Requirements\n\n- [Python 3.8](https://www.python.org/downloads/) or above\n- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)\n- [pdftoppm](https://poppler.freedesktop.org/)\n\n## Installation\n\nInstall Tesseract OCR and pdftoppm using your package manager. For example, on Ubuntu:\n\n```bash\nsudo apt install tesseract-ocr tesseract-ocr-all poppler-utils\n```\n\n### From PyPi\n\nInstall with pip:\n\n```bash\npython3 -m pip install --user pdf-language-detector\n```\n\nThen run directly from your terminal:\n\n```bash\npld --help\n````\n\n### From the sources\n\nClone the PLD repository:\n\n```bash\ngit clone git@github.com:github.com/icij/pld.git\n```\n\nInstall the required Python packages with poetry:\n\n```bash\npoetry install\n````\n\nThen run inside a virtual env managed by poetry:\n\n```bash\npoetry run pld --help\n````\n\n### From Docker\n\nInstall with Docker:\n\n```bash\ndocker pull icij/pld\n```\n\nThen run inside a container:\n\n```bash\ndocker run -it icij/pld pld --help\n```\n\n\n## Usage\n\n### Detect\n\nThis command process PDF files and detect the dominant language.\n\n```\npld detect --help\n\n    --language A list of ISO3 language codes to detect.\n    --input-dir: Path to the input directory containing PDF files. Default is the current directory.\n    --output-dir (optional): Path to the output directory. Default is 'out' directory in the current directory.\n    --max-pages (optional): Maximum number of pages to process per PDF file. Default is 5.\n    --resume (optional): Skip PDF files already analyzed.\n    --skip-images (optional): Skip the extraction of PDF files a images.\n    --skip-ocr (optional): Skip the OCR of images from PDF files.\n    --parallel (optional): Number of threads to run in parallel.\n```\n\n### Report\n\nThis command print a report from the previously detected language (using the same output dir).\n\n```\npld report --help\n\n    --output-dir: Path to the output directory. Default is 'out' directory in the current directory.\n```\n\n## Examples\n\nProcess PDF files in the current directory, detect English and Spanish languages, and save the results in the 'results' directory:\n\n```bash\npld --language eng --language spa --input-dir documents --output-dir results\n```\n\nProcess PDF files in the 'documents' directory, detect French and Greek languages, and limit the processing to 3 pages per file:\n\n```bash\npld --language fra --language ell --input-dir documents --max-pages 3\n```\n\n## License\n\nThis project is licensed under the MIT License.\n",
    'author': 'ICIJ',
    'author_email': 'engineering@icij.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
