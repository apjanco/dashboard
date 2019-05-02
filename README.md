# Exploring Texts from Russian Journals

*click on the image to load the interactive dashboard*
[![](https://github.com/apjanco/dashboard/raw/master/Screen%20Shot%202019-05-02%20at%207.52.57%20AM.png)](http://104.236.220.106:8000/)

This is a project to create a dashboard that will help a researcher at Ohio State University who studies Russian literary journals. Since the 1800s, journals have been a common way for many Russians to stay connected with contemporary culture.  In the 1970s and 1980s print runs were often over a million copies per issue. These "thick journals" are often 300-500 pages per issue (see [Bykov 2016](https://pdfs.semanticscholar.org/9cc6/7dc6af51ef662785251651b8a8aa166d3249.pdf)). Solzhenitsyn, for example, was first published in a thick journal.

There is a website in Russia called [Journal Room](http://magazines.russ.ru/) (*Zhurnal'nyi zal*) that has operated since the late 1990s and has the machine-readable text of 38 major thick journals beginning in 1992 to 2018. They recently posted that the site will no longer be updated. It is quite likely that the site will go offline in the near future. To save this remarkable resource, I scraped 76,296 texts from Journal Room.  Using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), I traversed the table of contents for each journal issue to record a text's author, title, genre, journal, year, issue and the full text of the piece (when available).  I have full text for 69,532 of the entries.  The full corpus is currently stored in a 5Gb MySql database. 

| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|*by journal* <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/apjanco/dashboard/raw/master/by_journal1.png">|*by genre* <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/apjanco/dashboard/raw/master/by_genre1.png">|
|*by author* <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/apjanco/dashboard/raw/master/by_author1.png">  |*by year*<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/apjanco/dashboard/raw/master/by_year.png">|

The chart above shows that the journals *Banner* and *New World* have, by far, the largest number of texts in the corpus.  By genre, the most prominent types of text are poetry (*stikhi*) and stories (*rasskazy*).  After cleaning the genre titles, poetry is clearly the most prominent genre of text. 

For current purposes, I created a CSV file of the text metadata, which can be downloaded from [here](https://haverford.box.com/shared/static/votuay8cy1uc7e61r27opxnynxb11sp3.csv).  The metadata dataset is free to use and distribute.  The full-text corpus contains content that could be restricted by Section IV of the Civil Code of the Russian Federation. Online content is largely interpreted by Russian law as an open space where content is subject to "free use" ([Sobol 2016](https://rm.coe.int/1680783347)). The footer of each page shows © 1996 - 2017 Journal Room. It would be worth contacting Journal Room before sharing the full dataset, but it is likely that use of the corpus for research falls under the legal understanding of "free use."     

*using the dashboard*

The dashboard is still a work in progress.  To reduce loading time, I have limited the dataset to the four most common journals.  The visualization makes it easy to see which authors published most with a particular publication.  The higher a point on the y-axis, the more texts an author published with that particular journal.  In theory, if that same author published in other journals, there are other points with that data.  In the future, it would be useful to produce bar graphs for each author with the relative number of publications in each journal.  At present, it is difficult to find any one author's points in the scatter plot.  

However, the current visualization is a valuable tool for identifying overlap in authors between journals.  The image below shows the near total lack of overlap between the authors published in *New World* as compared to *Friendship of the Peoples*.  This is expected given that *Friendship* published mostly non-Russian authors from the Soviet republics.  *New World* published more authors from the capitals. 

![](https://github.com/apjanco/dashboard/raw/master/Screen%20Shot%202019-05-02%20at%204.56.51%20AM.png)

By contrast, there is a great deal of overlap between the authors in *New World* and *Banner*. 

![](https://github.com/apjanco/dashboard/raw/master/Screen%20Shot%202019-05-02%20at%205.00.32%20AM.png) 

*technical details* 
The current dashboard was created with [Dash](https://plot.ly), which serves the plotly Python library using Flask and React.js. You can find the dashboard [here](http://104.236.220.106:8000/). I have also included [app.py](https://raw.githubusercontent.com/apjanco/dashboard/master/app.py) which will run locally with dash and pandas.  Just `pip install dash` in your preferred virtualenv, clone the repository, `cd dashboard` and then `$ python app.py`.  The current app is running with Flask. I am currently working to serve the application with nginx and uWsgi.  I have also experimented with [django-plotly-dash](https://github.com/GibbsConsulting/django-plotly-dash) for adding Dash apps to Django projects.       

The dashboard has three elements: a date slider, a datatable and a scatterplot.  I was not able to use a RangeSlider. The slider is currently working but selects a time period between the minimum value and the time selected.  The table displays the raw data and can be sorted and viewed with forward and backward buttons.  I would like to add a search field if possible.  

The scatterplot shows a point for each publication by an author in a journal.  Each column along the x-axis should show each of the journals that they published with along with the number of articles reflected in the y-axis. As the dates change in the slider, the callback function updates the dataframe used for the scatterplot.  

[app.py](https://raw.githubusercontent.com/apjanco/dashboard/master/app.py)
*based on example from the [Dash documentation](https://dash.plot.ly/getting-started-part-2)*
```python
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('slider', 'value')],
)
def update_figure(value):
    # uniqueYear is a list of year values, value is an index value for that list
    filtered_df = df[
        df.year.isin(list(uniqueYear[: value + 1]))
    ]  
    year = filtered_df['year'].value_counts().to_frame()

    traces = []
    for i in filtered_df.journal.unique():
        df_by_journal = filtered_df[
            filtered_df['journal'] == i
        ]
        traces.append(
            go.Scatter(
 
                # Here is the data for the x axis
                x=df_by_journal[
                    'author'
                ],  
                
                # Here is the data for the y axis
                y=df_by_journal[
                    'author'
                ].value_counts(),  
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {
                        'width': 0.5,
                        'color': 'white',
                    },
                },
                name=i,
            )
        )

```

## Scatter plots for text (scattertext)  

My project partner is particularly interested in relationships between texts, authors, and journals. Are there differences in the use of words and phrases (lexical features) that clearly distinguish one journal from another?  In order to visualize these differences, I am using a Python library called [scattertext](https://github.com/JasonKessler/scattertext) by Jason Kessler (see [Kessler 2017](https://arxiv.org/pdf/1703.00565.pdf)). The scattertext explorer creates a graph that helps to visualize what features most distinguish a text or category of texts from the rest of the dataset. For example, what terms best distinguish texts published in *Novyi mir* (*New World*) as opposed to all other journals?   

As an experiment, I created a script with scattertext that generates a visualization using the full text of articles and their journal of publication.  Scattertext uses [spaCy](https://spacy.io/modelsa) statistical language models. Russian is part of their multi-language model, but in testing, it provided poor results and often treated the text as Serbian or English. I found that the [Russian spaCy model from Yuri Baburov](https://github.com/buriy/spacy-ru) was far more accurate.  

Additionally, Scattertext has a very large memory footprint. The readme states that scattertext is only for "small-to-medium-sized corpora."  However, I was able to process the entire corpus.  It took three days using a machine with a 6-core Xeon processor and 64GB of RAM. One the first run it ran out of memory, so I created a 2TB swapfile. The process used as much as 100GB of memory.  The end result is a 10GB HTML file which I am not able to load in the browser.         

```python 
import scattertext as st
import spacy
import mysql.connector as sql
import pandas as pd
import numpy as np

# Create a connection to the MySql database server
db_connection = sql.connect(
    host='localhost', database='', user='', password=''
)

# Create a pandas dataframe from a sql query.  In this case we're selecting 100 random entries with text
df = pd.read_sql(
    "SELECT journal, title, text FROM catalog_tableofcontents WHERE text NOT LIKE '' ORDER BY RAND() LIMIT 100",
    con=db_connection,
)
df = df.replace(['', 'null'], [np.nan, np.nan])

# Load the spaCy Russian language model
nlp = spacy.load('spacy-ru/ru2')
nlp.add_pipe(nlp.create_pipe('sentencizer'))

# Create a scattertext object using the texts and journal categories.
corpus = st.CorpusFromPandas(
    df, category_col='journal', text_col='text', nlp=nlp
).build()

# Generate the D3 visualization
html = st.produce_scattertext_explorer(
    corpus,
    category='Новый Мир',
    category_name='Новый Мир',
    not_category_name='Other',
    width_in_pixels=1000,
    metadata=df['title'],
)

# Save the html to a file
open("full_output_novyi_mir.html", 'wb').write(
    html.encode('utf-8')
)
```

I tested various samples to find a threshold for the scattertext visualization.  Files with 1000 and 500 texts were too large to load in the browser.  A sample of 200 seems to be a good size for scattertexts. 

*How to read a scattertext visualization*
[![](https://github.com/apjanco/dashboard/raw/master/example.gif)](https://github.com/apjanco/dashboard/raw/master/example.gif) 

*Random sample of 100 texts comparing New World against all other journals. Click on the image to load the interactive page, please note that it takes 10-15 minutes to load in the browser*
[![](https://github.com/apjanco/dashboard/raw/master/textviz.jpg)](http://htmlpreview.github.io/?https://www.github.com/apjanco/dashboard/raw/master/sample100.html)

*Random sample of 200 texts comparing New World against all other journals. Image only.*
[![](https://github.com/apjanco/dashboard/raw/master/220_nzh.png)](https://github.com/apjanco/dashboard/raw/master/220_nzh.png)

Nonetheless, scattertext can be used to produce useful data about the entire text corpus.  Using the following, we can print out the 100 most distinctive terms for the journal *Novyi mir*.    
```python
term_freq_df = corpus.get_term_freq_df()
term_freq_df['Новый Мир freq'] = corpus.get_scaled_f_scores('Новый Мир')
pprint(list(term_freq_df.sort_values(by='Новый Мир freq', ascending=False).index[:100]))
```
This method can be repeated programmatically for all of the journals in the corpus using all of the texts and not just a sample.  This method can be applied to other categories simply by changing the value in `category_col` in CorpusFromPandas() to author, year, genre and so on.  What terms most distinguish poetry from verse?  What terms distinguish an author?    

*example of a plot for a single author. click for slow-loading interactive version.*
[![](https://github.com/apjanco/dashboard/raw/master/stepanov.png)](http://htmlpreview.github.io/?https://github.com/apjanco/dashboard/raw/master/output_stepanov.html)

*example plot for poetry*
[![](https://github.com/apjanco/dashboard/raw/master/poetry.png)](https://github.com/apjanco/zhz-dashboard/raw/master/poetry.png)

Another possible lead to follow is a library called [shifterator](https://github.com/ryanjgallagher/shifterator).  This is a package by a PhD student at Northeastern University.  It creates word shift graphs, which are "vertical bar charts that quantify which words contribute to a pairwise difference between two texts and how they contribute."  This seems like a promising lead, but the library is still under development and still needs to be packaged. Before a word shift graph could be generated, I would also need to write a script to process the texts and return dictionaries with "word types as keys and frequencies as values." The example graphs for shifterator are compelling and could offer an effective alternative to scattertext.  However, given the problems faced by scattertext's reliance on D3 in the browser and the amount of data being plotted, bqplot, matplotlib or plotly may be better options. 

*example word shift graph from shifterator*
![](https://github.com/ryanjgallagher/shifterator/raw/master/figures/presidential-speeches_smaller.png)

