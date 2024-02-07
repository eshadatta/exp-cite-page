import helpers.utilities as u
import pytest
import frontmatter
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler

# tests function to get title from markdown file
def test_valid_file():
    valid_file = "tests/fixtures/tiny_static_site/content/report/rules.md"
    md = u.read_markdown_file(valid_file)
    file_title = md.metadata['title']
    try:
        title = u.get_md_title(valid_file, md)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
    assert file_title == title

def test_invalid_file():
    invalid_file = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_multiple_dois.json"
    file_contents = u.read_markdown_file(invalid_file)
    with pytest.raises(ValueError) as e:
        u.get_md_title(invalid_file, file_contents)

    

