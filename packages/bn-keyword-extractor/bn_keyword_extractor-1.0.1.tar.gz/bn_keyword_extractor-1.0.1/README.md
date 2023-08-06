# Run using below code

```python
!pip install -r requirements.txt

from keyword_extractor.keyword_extractor import KeywordExtractor
# Example usage
extractor = KeywordExtractor()
text = 'আমি বাংলায় গান শোনা ভালবাসি।'
keywords = extractor.extract_keywords(text)
print(keywords)
```
