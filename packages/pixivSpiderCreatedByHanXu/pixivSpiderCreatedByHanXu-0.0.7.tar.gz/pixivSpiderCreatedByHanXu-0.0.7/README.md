# Make sure that your internet can visit the foreign websites.
- The package has one module to use.

# Easy use
```python
import pixivSpiderCreatedByHanXu as Spider
if __name__ == '__main__':
    ex=Spider.pixiv_spider()
    ex()
```

# Module:pixivSpiderCreatedByHanXu
- The module has two ways to crawl images:`Rank` and `keyword`.
## search by `Rank`
- Looking at the following example:
```shell
{'1': 'Rank', '2': 'Keyword'}
Type in the target you want to search.
1
{'1': 'Simple:Recommended and Fast because the downloaded images are vague.You can view the simple image and select what you love', '2': 'Specific:Not Recommended and Slow because the downloaded images are clear'}
Type in the requirement of download-mode.
1
type in the path where you want to reserve the images:
rank20230424
Type in the number of images you want:
5
{'1': 'daily', '2': 'weekly', '3': 'monthly', '4': 'rookie', '5': 'daily_ai', '6': 'male', '7': 'female'}
type in the searchMode you want
1
Type in the date you want to search.Follow the format like this:20230423
20230424
```

## search by `keyword`
```shell
{'1': 'Rank', '2': 'Keyword'}
Type in the target you want to search.
2
{'1': 'Simple:Recommended and Fast because the downloaded images are vague.You can view the simple image and select what you love', '2': 'Specific:Not Recommended and Slow because the downloaded images are clear'}
Type in the requirement of download-mode.
1
type in the path where you want to reserve the images:
秋山澪图片
Type in the number of images you want:
5
{'1': '500', '2': '1000', '3': '5000', '4': '10000'}
Type in the requirement of heat.Larger the number is,Less the results are.
2
type in the keywords used to search in pixiv:
秋山澪
```
# Download
```shell
pip install pixivSpiderCreatedByHanXu
```