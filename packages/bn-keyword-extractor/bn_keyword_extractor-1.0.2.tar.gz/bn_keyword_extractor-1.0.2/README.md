# Run using below code

```python
!pip install bn-keyword-extractor

from keyword_extractor import KeywordExtractor
extractor = KeywordExtractor()
text = "আমি বাংলায় গান শোনা ভালবাসি।"
keywords = extractor.extract_keywords(text)
print(keywords) 
```
Output: ['শোনা', 'ভালবাসি', 'বাংলায়', 'গান']
