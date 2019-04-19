# Introduction

*click on the image to load the interactive dashboard*
[![](https://github.com/apjanco/dashboard/raw/master/Screen%20Shot%202019-04-11%20at%202.57.13%20PM.png)](http://104.236.220.106:8000/)

This is a project to create a research dashboard that will help a researcher at Ohio State University who studies Russian literary journals. Since the 1800s, journals have been the most affordable way for many Russian to stay connected with contemporary culture.  In the 1970s and 1980s print runs were often over a million copies per issue. Solzhenitysn, for example, was first published in a thick journal.  The common name these large, often 300-500 page long, journals is a "thick journal" (see, [Bykov 2016](https://pdfs.semanticscholar.org/9cc6/7dc6af51ef662785251651b8a8aa166d3249.pdf)).

There is a web-site in Russia called [Journal Room](http://magazines.russ.ru/) (*Zhurnalnyi zal'*) that has operated since the late 1990s and has the machine-readable text of 38 thick journals starting from 1992 to 2017. They recently posted that the site will no longer be updated. It is quite likely that the site will go offline in the near future.  The current dataset is compsed of 76,296 texts that I scraped from Journal Room.  Using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), I traversed the table of contents for each journal issue to record a text's author, title, genre, journal, year, and the full text of the piece (when available).  I have full text for all but 6,764 of the entries.

*entries by journal and genre*
![](https://github.com/apjanco/dashboard/raw/master/2graphs.gif)
For those that do not speak Russian.  The chart above shows that the journals Banner and New World have, by far, the largest number of texts in the corpus.  By genre, the most prominent types of text are poetry (*stizhi* and *stizhotvoreniia*), stories (*rasskaz* and *povest'*).  Further normalization of the genre titles would lend better results.    

For current purposes, I creates a csv file of the text metadata, which can be downloaded [here](https://haverford.box.com/shared/static/jwp9pd68ffl7tneh9hjob943ikcqg6x4.csv).  The metadata dataset is free to use and distribute.  The fulltext corpus contains content that could be, but is unlikely, restricted by Section IV of the Civil Code of the Russian Federation. Online content is largely interpreted by Russian law as an open space where content is subject to "free use"([Sobol, 2016](https://rm.coe.int/1680783347)). The footer of each page shows `© 1996 - 2017 Journal Room` and the site lists a contact. Further research is required, and it would be worth contacting Journal Room before sharing the full dataset, but it is likely that use of the corpus for research falls under the legal understanding of "free use."     

The current dashboard was created with [Dash](https://plot.ly), which serves the plotly Python library using Flask and React.js.  I have included [app.py](https://raw.githubusercontent.com/apjanco/dashboard/master/app.py) which will run locally with dash and pandas.  Just `pip install dash` in your prefered virtualenv, clone the repository, `cd dashboard` and then `$ python app.py`.  I am currently working on serving the application with nginx and uWsgi.  I have also experimented with a Django app for adding Dash apps to Django projects.  I hope to have these working soon.  I have had a lot of trouble with Idyll and bqplot.  I tried, but was not able to run dash in a jupyter notebook.       

The dashboard has three elements, a date slider, a datatable and a scatterplot.  I plan to change the date slider to select a time range.  It is currently working, but selects a time period between the minimum value and the time selected.  The table displays the raw data and can be sorted and viewed with forward and backward buttons.  I would like to add a search field if possible.  The scatterplot shows the number of total articles on the y axis and authors' names on the x axis.  The points are color coded by journal.  This makes it possible to identify clusers of authors that are all associated with a common journal.  This is a key interest for my researcher.  It is possible to zoom in on a particular cluster to see the names of the authors and the journal on hover.   

My project partner is particularly interested in the relationships between texts, authors and journals. Are there differences in the use of words and phrases (lexical features) that clearly distinguish one journal from another?  In order to visualize these differences, I am using a Python library called [scattertext](https://github.com/JasonKessler/scattertext).  The scattertext explorer creates a graph that helps to visualize what features most distinguish a text or category of texts from the rest of the dataset. For example, what terms best distinguish texts published in *Novyi mir* (New World) as opposed to all other journals?   

*click on the image to load the interactive page, please note that is takes 10-15 minutes to load in the browser*
[![](https://github.com/apjanco/dashboard/raw/master/textviz.jpg)](http://htmlpreview.github.io/?https://www.github.com/apjanco/dashboard/raw/master/sample100.html)

As an experiment, I created a script with scattertext that generates a visualization using the full text of articles from the corpus and their journal of publication.  Scattertext uses [spaCy](https://spacy.io/modelsa) language models.  Russian is part of their multi-language model, but in testing it provided poor results and often treated the text as Serbian or English.  I found that the [Russian spaCy model from Yuri Baburov](https://github.com/buriy/spacy-ru) was far more accurate.  

Addionally, Scattertext has a very large memory footprint. The readme states that scattertext is only for "small-to-medium-sized corpora."  I was able to process the entire corpus.  It took three days using a machine with a 6-core Xeon processor and 64GB of RAM. One the first run it ran out of memory, so I created a 2TB swapfile, The process used as much as 100GB of memory.  The end result is a 10GB html file which I am not able to load in the browser.         

```python 
import scattertext as st
import spacy
from pprint import pprint
import mysql.connector as sql
import pandas as pd
import numpy as np

db_connection = sql.connect(host='localhost', database='', user='', password='')

df = pd.read_sql("SELECT journal, title, text FROM catalog_tableofcontents WHERE text NOT LIKE '' ORDER BY RAND() LIMIT 100", con=db_connection)
df = df.replace(['', 'null'], [np.nan, np.nan])
nlp = spacy.load('spacy-ru/ru2')
nlp.add_pipe(nlp.create_pipe('sentencizer'))

corpus = st.CorpusFromPandas(df,
                             category_col='journal',
                             text_col='text',
                             nlp=nlp).build()

html = st.produce_scattertext_explorer(corpus,
          category='Новый Мир',
          category_name='Новый Мир',
          not_category_name='Other',
          width_in_pixels=1000,
          metadata=df['title'])
open("full_output_novyi_mir.html", 'wb').write(html.encode('utf-8'))
```

Given the problems using scattertext on larger corpora, another possible lead to follow is a library called [shifterator](https://github.com/ryanjgallagher/shifterator).  This is a package for creating word shift graphs, which are "vertical bart charts that quantify which words contribute to a pairwise difference between two texts and how they contribute."  This seems like a promising lead, but the library is still under development and still needs to be packaged. Before a word shift graph could be generated, I will also need to write a script to process the texts and return dictionaries with "word types as keys and frequencies as values." The example graphs for shifterator are compelling and could offer an effective alternative to scattertext.  However, given the problems faced by scattertext's reliance on D3 in the browser and the amount of data being plotted, bqplot, matplotlib or plotly may be better options. 

*example word shift graph from shifterator*
![](https://github.com/ryanjgallagher/shifterator/raw/master/figures/presidential-speeches_smaller.png)

