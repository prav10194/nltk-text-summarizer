# nltk-text-summarizer
Summarize articles on the net by simply copying the intended article.

This was built in Python 3.4 and please refer to the pre-requistes required for running it successfully. If you are on Linux/iOS you will experience problem in creating system notifications. Will update the code for that soon. 

Pre-requisites - 
-------
1. Python 3.4 (although it shoudn't have problem running on other Python versions.)
2. NLTK for Python 
3. nltk.corpus

Usage - 
-------

1. Clone/Download zip of TextSummarizer
2. Extract content of the zip.
3. Open IDLE/cmd to run the following code - 
```python
import os
os.chdir('path') #path where script is saved.

from textSummarize import ExtractNewSentences
ExtractNewSentences().run() #by default the script runs for 2 hours in background with 75% summarization of text.

#To run for specific hour(s) say 1.5 hours
ExtractNewSentences().run(timer=1.5)

#To summarize say 50% of the text
ExtractNewSentences().run(reducepercent=0.5)

```
To stop script, simply close the screen or press CTRL+C

Steps to install nltk -

1. Extract the zip content
2. Open cmd
3. Run the following commands -
```cmd
cd "folderpath where zip is extracted"
python setup.py install
```

For nltk_data -

1. Extract the folder and save it in your python directory.
