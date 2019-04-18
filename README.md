# dashboard

[![](https://github.com/apjanco/dashboard/raw/master/Screen%20Shot%202019-04-11%20at%202.57.13%20PM.png)](http://104.236.220.106:8000/)

This is a work in progress.  The end goal is a research dashboard that will help a researcher who studies Russian literary journals that feature poetry, essays and other writing. In the Soviet period, journals were the most affordable way to stay connected with contemporary culture and print runs were often over a million copies per issue. Solzhenitysn, for example, was first published in a thick journal.

There is a web-site in Russia called [Journal Room](http://magazines.russ.ru/) (*Zhurnalnyi zal'*) that has operated since the late 1990s and has the full text of 38 thick journals. They recently posted that the site will no longer be updated. It is quite likely that the site will go offline in the near future.  The current dataset is compsed of 76,296 texts that I scraped from Journal Room.  Using beautifulSoup, I traversed the table of contents for each journal issue to record a text's author, title, genre, journal, year, and the full text of the piece (when available).  I have full text for all but 6,764 of the entries.  For current purposes, I creates a csv file of the text metadata, which can be downloaded [here](https://haverford.box.com/shared/static/jwp9pd68ffl7tneh9hjob943ikcqg6x4.csv).  The metadata dataset is free to use and distribute.  The fulltext corpus contains content that could be, but is unlikely, restricted by Section IV of the Civil Code of the Russian Federation. Online content is largely interpreted by Russian law as an open space where content is subject to "free use"([Sobol, 2016](https://rm.coe.int/1680783347)). The footer of each page shows `© 1996 - 2017 Journal Room` and the site lists a contact. Further research is required, and it would be worth contacting Journal Room before sharing the full dataset, but it is likely that use of the corpus for research falls under the legal understanding of "free use."     

The current dashboard was created with [Dash](https://plot.ly), which serves the plotly Python library using Flask and React.js.  I have included [app.py](https://raw.githubusercontent.com/apjanco/dashboard/master/app.py) which will run locally with dash and pandas.  Just `pip install dash` in your prefered virtualenv, clone the repository, `cd dashboard` and then `$ python app.py`.  I am currently working on serving the application with nginx and uWsgi.  I have also experimented with a Django app for adding Dash apps to Django projects.  I hope to have these working soon.  I have had a lot of trouble with Idyll and bqplot.  I tried, but was not able to run dash in a jupyter notebook.       

The dashboard has three elements, a date slider, a datatable and a scatterplot.  I plan to change the date slider to select a time range.  It is currently working, but selects a time period between the minimum value and the time selected.  The table displays the raw data and can be sorted and viewed with forward and backward buttons.  I would like to add a search field if possible.  The scatterplot shows the number of total articles on the y axis and authors' names on the x axis.  The points are color coded by journal.  This makes it possible to identify clusers of authors that are all associated with a common journal.  This is a key interest for my researcher.  It is possible to zoom in on a particular cluster to see the names of the authors and the journal on hover.   

My project partner is particularly interested in the relationships between texts, authors and journals.  How do networks of authors explain similarities in the texts published by a particular journal?  Are there differences in the use of words and phrases (lexical features) that clearly distinguish one journal from another?  In order to visualize these differences, I am using a Python library called [scattertext](https://github.com/JasonKessler/scattertext).  The scattertext explorer creates a graph that helps to visualize what features most distinguish a text or category of texts from the rest of the dataset. For example, what terms best distinguish texts published in *Novyi mir* (New World) as opposed to all other journals?   

![](https://github.com/apjanco/dashboard/raw/master/textviz.jpg)

As an experiment, I created a script with scattertext that generates a visualization using the full text of articles from the corpus and their journal of publication.  Scattertext uses [spaCy](https://spacy.io/modelsa) language models.  Russian is part of their multi-language model, but in testing it provided poor results and often treated the text as Serbian or English.  I found that the [Russian spaCy model from Yuri Baburov](https://github.com/buriy/spacy-ru) was far more accurate.  

Addionally, Scattertext has a very large memory footprint. I have only successfully created a visualization for a random sample of 100 texts.  The readme states that scattertext is only for "small-to-medium-sized corpora."  At the time of writing, I am still trying to run the script for the full corpus.  It has been running for 116 hours on a machine with a 6-core Xeon processor and 64GB of RAM.  I created a 2TB swapfile and the process is currently using 100GB of memory.       

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

