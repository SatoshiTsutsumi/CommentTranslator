# CommentTranslator
Simple translator for program comments

# Prerequisites
- comment-parser [comment-parser](https://pypi.org/project/comment-parser/)
- libmagic
- DeepL API Key [DeepL API](https://www.deepl.com/en/docs-api)


# Spec
## Support programming languages (use MIME)
|  Language  |  MIME  |
| ---- | ---- |
|C	   |text/x-c
|C++/C#|text/x-c++
|Go	   |text/x-go
|HTML  |text/html
|Java  |text/x-java-source
|Javascript|application/javascript
|Python|text/x-python
|Ruby  |text/x-ruby
|Shell |text/x-shellscript
|XML   |text/xml

## Support comment languages
[Translatable Languages](https://www.deepl.com/docs-api/translate-text/large-volumes/)

## Support comment style
Single-line comment (multi-line comment will be supported in the future release)

# How to use
Note that trans_comment.py translate files **In-Place** manner. You should backup files before using the script.

```
$ DEEPL_API_KEY="xxx" python trans_comment.py \
   --ext java --mime text/x-java-source \
   --source_lang ZH \
   --target_lang EN \
   --verbose
   path_to_target  
```
