The summarization of research articles is a complex task compared to general-purpose summaries.This is a result of
the distict nature or semantic structure of these scientific articles. The presence of inline citations and summarization
modules bias to certain Text features that often work well on less-tecnical text but fail to produce coherence in 
this area are all underlying factors.

We circumvent these challenges in order to produce more coherent, human-understandable summaries of manuscripts and research text
using this libary.


## Installation
You can easily install the package using the ```pip``` command:

 ```
   pip install articlesumm
 ```

## Usage
The package takes a string as input(specify a path/directory for an article or alternatively pass a string as a variable). The tokenization of the sentences and words can be performed with the first function: 

```
  parse=purge(text)
  type(parse) 

  #tuple
```

Alternatively, you can tokenize the sentences and words with any other technique and pass the processed text to the summarization model.

## Example
```
  text='''TextRank is a graph-based ranking model for text processing which can be used in order to find the most relevant sentences in text and also to find keywords. The algorithm is explained in detail in the paper at https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf . In order to find the most relevant sentences in text, a graph is constructed where the vertices of the graph represent each sentence in a document and the edges between sentences are based on content overlap, namely by calculating the number of words that 2 sentences have in common.'''

  from ArticleSumm import purge
  from ArticleSumm import summarizer

  parse=purge(text)

  #summary=summarizer(text,parse[0], parse[1], summary_length=3)
  summary=summarizer(text,words=purge(text)[0], sentence_list=purge(text)[1], summary_length=3)
  print(summary)


```
