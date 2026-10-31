"""Reference extraction must preserve source labels without inventing metadata."""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

spec = spec_from_file_location('article_sources', Path(__file__).parents[1] / 'build/article_sources.py')
module = module_from_spec(spec)
spec.loader.exec_module(module)


def test_sources_exclude_examples_code_images_and_duplicate_urls():
    text = '''[Repo](https://github.com/org/repo)
    [Again](https://github.com/org/repo)
    ![Image](https://host/image.png)
    [Example](https://example.com/)
    ```python
    [Code sample](https://github.com/placeholder/example)
    ```
    [Original post](https://www.linkedin.com/posts/example)
    '''
    records = module.sources(text)
    assert len(records) == 2
    assert records[0]['author'] == 'org'
    assert records[1]['author'] == ''
    assert all('date' not in record for record in records)
