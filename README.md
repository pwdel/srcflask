# srcflask

Running custom source code from within a secure flask app.

# Objective

Hello World.

# Planning Out App and Location to Store Source

### Two Objectives

The idea behind storing source code in a specific location is two-fold:

1. To deploy an extremely simple machine learning application, with one set model stored on the server itself is like storing an image on the server itself. 

2. To reserve an area where we can store files which help interact with a future data management system which is likely to be more complex. There are existing tools and plugins which could be used, as well as the capability to build our own, which would involve perhaps building a new database table which points toward stored S3 objects.  Either way, it seems like an area of the overall app to keep, "machine learningy type stuff" would be good to have apart from the rest of the application.

Servers are not as ideal for storing massive amounts of data like large picture or video stores. Heroku in particular is extremely limited with only a 500MB total slug size.  SSD drives have faster response time but are more expensive than HDD or glacial storage.

### Discussion on Scalability for Model Storage

[Discussion on best practices to store Python machine Learning Models](https://datascience.stackexchange.com/questions/19802/best-practices-to-store-python-machine-learning-models).

> Store them in document storage (eg. mongoDB) - this method is recommended when your model files are less then 16Mb (or the joblib shards are), then you can store model as binary data. in addition, some ML libraries support model export and import in json (eg. LightGBM), which makes it a perfect candidate for storage in document storage. Advantages: easy tracking of model generation and easy access, Disadvantages: things will get messy if model object is too large.

> Store your model on object storage (eg. Amazon S3) - this method is good if your models are very large, in this case you get unlimited storage and fairly easy API, you pay more, that is for sure. Advantages: Unlimited space and ability to store arbitrary file formats. Disadvantages: cost, and the fact that to do it right you'll need to develop your own tracking system.

An additional resource related to data engineering is here:

* [Slideshare on Data Engineering for ML Asset Management](https://www.slideshare.net/paulvermont/2018-data-engineering-for-ml-asset-management-for-features-and-models)

Basically, there are multiple different data version control open source projects.

The main Open Source platform appears to be:

* [Data Version Control - Github](https://github.com/iterative/dvc)  - [Data Version Control Pypi](https://pypi.org/project/dvc/)

https://dvc.org/

>     Simple command line Git-like experience. Does not require installing and maintaining any databases. Does not depend on any proprietary online services.
>    Management and versioning of datasets and machine learning models. Data is saved in S3, Google cloud, Azure, Alibaba cloud, SSH server, HDFS, or even local HDD RAID.
>    Makes projects reproducible and shareable; helping to answer questions about how a model was built.
>    Helps manage experiments with Git tags/branches and metrics tracking.



Other platforms include:

* [Quilt PyPi](https://pypi.org/project/quilt3/) or [Quilt Github](https://github.com/quiltdata/quilt) is designed to create versioned datasets with S3.
* https://vespa.ai/ (also open source)
* https://polyaxon.com/
* https://www.seldon.io/

### Following the Normal Convention for ML Source Code

* This [towards data science post](https://towardsdatascience.com/organizing-machine-learning-projects-e4f86f9fdd9c) goes through sorting different aspects of a smaller data science project into .py files held within /src.
* This [blog article on data science project folder structure](https://dzone.com/articles/data-science-project-folder-structure) goes through an expanded definition of structuring data beyond just data processing held in src.
* [This article also goes through project structure options](https://towardsdatascience.com/manage-your-data-science-project-structure-in-early-stage-95f91d4d0600)

Our entire project structure looks like the following:


```
├── .env.dev

├── .env.prod

├── .env.prod.db

├── .gitignore

├── docker-compose.prod.yml

├── docker-compose.yml

└── services

	├── nginx

	│   	├── Dockerfile

	│   	└── nginx.conf

	└── web

	    	├── Dockerfile

    		├── Dockerfile.prod

    		├── entrypoint.prod.sh

    		├── entrypoint.sh

    		├── manage.py

     		├── requirements.txt

    		├── project

    			├── __init__.py

    			├── assets.py

    			├── auth.py

    			├── forms.py
    			
    			├── models.py

    			├── routes.py

    			├── config.py

    			└── static

	    			├── /css

	    			├── /dist

	    			├── /img

	    			├── /src

		    			└── js

	    			└── style.css	    			

    			└── /templates
```
Zooming in on the /static/src folder, we have:

```
└── src

│	├── features

│	├── preperation

│	├── preprocessing

│	├── evaluation

│	└──	js

└── tests

│	└──	unit_tests

└── models

│	├── seedmodels

│	└──	retrainedmodels

└── data

│	├──	raw_data

│	├──	processed_data

│	└──	user_input_data

└── pipeline

│	└──	model_retraining_automation_scripts

└── docs

	├──	Documentation

	└──	Notebooks


```

>     project_name: Name of the project.
>    src: The folder that consists of the source code related to data gathering, data preparation, feature extraction, etc.
>    tests: The folder that consists of the code representing unit tests for code maintained with the src folder.
>    models: The folder that consists of files representing trained/retrained models as part of build jobs, etc. The model names can be appropriately set as projectname_date_time or project_build_id (in case the model is created as part of build jobs). Another approach is to store the model files in a separate storage such as AWS S3, Google Cloud Storage, or any other form of storage.
>    data: The folder consists of data used for model training/retraining. The data could also be stored in a separate storage system.
>    pipeline: The folder consists of code that's used for retraining and testing the model in an automated manner. These could be docker containers related code, scripts, workflow related code, etc.
>    docs: The folder that consists of code related to the product requirement specifications (PRS), technical design specifications (TDS), etc.

> preparation: Data ingestion such as retrieving data from CSV, relational database, NoSQL, Hadoop etc. We have to retrieve data from multiple sources all the time so we better to have a dedicated function for data retrieval.
> processing: Data transformation as source data do not fit what model needs all the time. Ideally, we have clean data but I never get it. You may say that we should have data engineering team helps on data transformation. However, we may not know what we need under studying data. One of the important requirement is both off-line training and online prediction should use same pipeline to reduce misalignment.
> modeling: Model building such as tackling classification problem. It should not just include model training part but also evaluation part. On the other hand, we have to think about multiple models scenario. Typical use case is ensemble model such as combing Logistic Regression model and Neural Network model.
> Test case for asserting python source code. Make sure no bug when changing code. Rather than using manual testing, automatic testing is an essential puzzle of successful project. Teammates will have confidence to modify code assuming that test case help to validate code change do not break previous usage.
> Storing intermediate result in here only. For long term, it should be stored in model repository separately. Besides binary model, you should also store model metadata such as date, size of training data.
> processed: To shorten model training time, it is a good idea to persist processed data. It should be generated from “processing” folder.

The above descriptions can be transitioned over to a database management system, using perhaps a relational database which points over to the proper datastores held in an S3 or similar document based storage system (or object based storage system for that matter).

* [I wrote a Stackoverflow Answer to a question someone had here](https://stackoverflow.com/questions/60299143/folder-structure-of-flask-app-with-machine-learning-component/67100486#67100486).

### Going Beyond Monolithic Applications

In a seperate repo, I have worked on putting together a Jupyter notebook which runs on a Docker container.  This is one hypothetical way that the above monolithic application all contained within one container could be seperated out into its own container.

[This blogpost from Neptune.ai](https://neptune.ai/blog/data-science-machine-learning-in-containers) goes through using Docker Swarm as a way to orchestrate a multi-container machine learning system.  Using this type of approach, a load balancer can be used to access multiple different servers to create a sort of, "elastic compute" type system that expands based upon the number of users accessing a system, or load on a system.

Of course hypothetically different machine learning processes could be designed to rest on different types of servers, which might cost more or less depending upon the power of the server, and might get more or less use depending upon what algorithm is being run - this would be another reason for possibly organizing a Swarm or Kubernetes style architecture with multiple containers.

All of this one might categorize under the field of, "High Availability Enterprise," development.

# Picking a Model to Work With

For this demonstration, all that is needed is a simple machine learning model that will work with some of the data structures that we already have on hand and have been working with in this project thus far.

The eventual goal is to create an automatic text generation application, based upon inputs from the user, which perhaps includes utilization of text information from the web. A sketch of what the imagined overall obejctive is:

![ML Text Generation Architecture Draft](/readme_img/ml-arch01.png)

* Previous learnings about what the actual algorithm may be can be found [in this repo](https://github.com/pwdel/textgeneratornotes) as well as [this repo](https://github.com/pwdel/nvidialubuntutensorflow) which I authored.

Using [Diagram.io](https://www.dbdesigner.net/) I can start to map out a hypothetical expanded database which would store what we are looking to build above.

![Draft RDB Design](/readme_img/rdb_design01.png)

# Initial Deployment Work

## Background

The most recent work I have done to make a machine learning model deployment possible can be found [here at this github repo](https://github.com/pwdel/flasksecurity).

This application contains all of the necessary foundation for putting together an basic flask application with users and an administrator which controls user access.

Leveraging that codebase, I can basically build a new system that auto-generates text based upon user document creation and creates automatically generated snippets based upon text inputs (of a fixed length).

As discussed in a [previous Github repo](https://github.com/pwdel/textgeneratornotes), the method used to generate text will be:

* We are using a pre-trained GPT2 dataset
* gpt2tokenizer
* tfgpt2lmheadmodel
* Beam search

[Notebook example using the above method](https://github.com/pwdel/textgeneratornotes/blob/main/notebooks/textgeneration.ipynb).

## Copying and Pasting the Code and Starting Off

### Copy/Pasting Code

Basically I just copy the "services" and .yml files as is from the /flasksecurity project folder.

### Setting Up Project Structure Above

Within /static, I set up the following folders as planned above:

![Project Structure](/readme_img/projectstructure.png)

# Building New Database Table(s)

## Previous Work

My [userlevelmodelsflask repo](https://github.com/pwdel/userlevelmodelsflask#document-model) goes through how the document model was created and what steps were taken to build tables from scratch within the models.py file.

## Keeping Project Elements Separate

Since at this point I'm essentially writing software on top of a previously existing app which dealt with user interfacing and document creation, it would be good to know whether I could build out all of my code, including the new data models in new folders, beyond models.py.

* [This Stackexchange Answer](https://stackoverflow.com/questions/14789668/separate-sqlalchemy-models-by-file-in-flask) asks about Separate SQLAlchemy models by file in Flask and points to:
* [This Stackexcange Q&A](https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045) responds to the previous one.

The two new classes that are being created to generate tables are:

* renditions
* autodocs

The, "autodocs" are automatically generated documents, while, "renditions" is a helper table that points to the original document that each autodoc is coming from.

Where do these new tables rightfully fit in our project structure?  Trying our best to keep with organizational best practices, the, "documents" and "retentions" within our original model.py should probably go within, "data/userinputdata," but for project simplification purposes I will probably just keep them in models.py.

As discussed above, the really, "proper" way to organize everything would be to put each, "section" of the app into a seperate container and have those containers communicate to each other via API's. However that is perhaps work for another time.

### Rough Plan

* If there is any need for pre-processing, perhaps a table for data features being extracted, that could perhaps go into, "/data/processeddata"
* As mentioned above, hypothetically documents and retentions should be in, "data/userinputdata" but we will skip that for now.
* "/data/rawdata" can probably remain empty for now, there isn't really any raw data coming in that is pre-processed - un less of course we create a holding area for document text which prior to any further processing needed.
* autodocs and renditions will probably best fit within, "processeddata" as this is basically an output from the model.

Of course the data itself are not stored in these folders, they are stored in the RDB, but the classes describing this data is stored within these folders.

### Autodocsmodels.py

This is similar to models.py, but it is where the autodocs table will be described.

Of course using SQLAlchemy, there will be callbacks from models.py to autodocsmodels.py and vice versa, so not everything is 100% clean.

#### Creating the Database Through Importing the Model

Within __init__.py:

```
# activate SQLAlchemy
db = SQLAlchemy()
...

    # initialize database plugin
    db.init_app(app)

    ...

        # Create Database Models
        db.create_all()
```
The important thing seems to be that within the init file, the model class gets created by grabbing from the project folder, and importing models.  This allows database models to be created with "db.create_all()" right below it.

```
        # import model class
        from . import models
```
So hypothetically to import a new autodocsmodels.py class, we could do:

```
        # import users and documents model class
        from . import models
        # import autodocs and revisions model class
        from /static/data/processeddata/autodocsmodels.py import autodocsmodels
```
Of course that would not work, as that's not how importing works - we have to create a package.

The, "right" way to do imports is to create packages, [per this guide here](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html) and as [this stackoverflow document talks about](https://stackoverflow.com/questions/4383571/importing-files-from-different-folder). 

Basically, we need to create an __init__.py file within the folder, "processeddata", per stackoverflow:

>  Its very existence tells Python to treat the directory as a package.


```
└── static

	└── __init__.py

	└── data

		├── __init__.py

		├──	raw_data

		└──	processeddata

			└── __init__.py

		└──	userinputdata
```

Assuming the above, we should be able to register the model with the following within the main __init__.py

```
from static.data.processeddata import autodocsmodels
```
When we try the above and attempt to build, we get the following error:

```
flask  |     from static.data.processeddata import autodocsmodels
flask  | ModuleNotFoundError: No module named 'static'
```
From Stackoverflow:

> what happens with python is that all python files are treated as modules and the folders with an init.py file are treated as packages

[Python Package and Module Documentation for Python 3](https://docs.python.org/3/tutorial/modules.html#packages) is found there.

Could try another method:

```
import static.data.processeddata.autodocsmodels
```
This also resulted in a ModuleNotFoundError.  Could it be that the top directory containing the original, main __init__.py file needs to be a part of this string?  The python3 documentation appears to suggest so.

So the following format works:

```
        # import autodocs and revisions model class
        import project.static.data.processeddata.autodocsmodels
```
Another way to import this would be:

```
        # import autodocs and revisions model class
        from project.static.data.processeddata import autodocsmodels
```

## Building the Model

So once we are able to successfully import the audodocsmodels.py file, we can then build the table in a similar way that we did at models.py.

We import the following at the top:

```
"""Database models."""
from . import db
from flask_login import UserMixin, _compat
from flask_login._compat import text_type
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

```
Then create a sample table like so:

```
"""Autodoc Object"""
class Autodoc(db.Model):
    """Autodoc model."""
    """Describes table which includes autodocs."""

    __tablename__ = 'autodocs'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    body = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """backreferences Document class on revisions table"""
    documents = relationship(
        'Revision',
        back_populates='autodoc'
        )

```
Note the backpopulation to autodoc when referring to the documents object within the relationship function. The, "Revision" class has similar relationship properties, and a back relationship is also added to the Document class in models.py.

Importing is a big more complex since we have a bit more complex folder structure now.  Within autodocmodels.py we have to import as shown:

* "from project import db" rather than from . import db - the "." character represents the same or home directory, in this case we have to be explicit and point back to the parent directory by explicitly calling out, "project."

Within the models.py file we had to import at length as shown above, the final result was:

```
# import autodocsmodels.py
from project.static.data.processeddata import autodocsmodels
from project.static.data.processeddata.autodocsmodels import Autodoc, Revision

```

Ensuring that our data table and list of relations works, we log into postgres:

```
               List of relations
 Schema |    Name    | Type  |      Owner       
--------+------------+-------+------------------
 public | autodocs   | table | userlevels_flask
 public | documents  | table | userlevels_flask
 public | retentions | table | userlevels_flask
 public | revisions  | table | userlevels_flask
 public | users      | table | userlevels_flask

```
We are now ready to fill autodocs with text and attach/assign them to documents.

# Cleaning Human Input Data

### Starting off And Ensuring Data Writes Work - Architecture

To make sure that all of the data writes as expected at the appropriate time, we need to write some kind of dummy autodocs before populating the cells within the table with our autogenerated text, and then display that result to users.

The rules for this population should be as follows:

1. Whenever a user/sponsor creates a new document (document x), an autodoc (autodoc y) should be generated along with it.
2. Autodoc y gets associated with autodoc x via the revisions table.
3. After a document has been created, any time a document is edited/saved, a new autodoc is created.

So again working with the principal of keeping the relevant code in the relevant part of the application to the best of our ability, there are going to be some modules which get created that exist in the proper project structure, but perhaps get called in the previous base app structure.

For now, our autodoc model will be simple, perhaps just writing a, 'hello world' string to a cell.  However, this function in it of itself is an autodoc, so we should still figure out where to put this.

### General Overview on File and Folder Organization

Looking ahead toward the rest of this project, here is a general plan where we could put various elements of the machine learning code.

A new file, "autodocwriter.py" could go under /src/evaluation since it's basically where a model does evaluation on input text.

```
└── src

│	├── features

│		├──	__init__.py

│		└──	doctokenization.py

│	├── preperation

│	├── preprocessing

│	├── evaluation

│		├──	__init__.py

│		└──	autodocwriter.py

│	└──	js


...

└── models

│	├── seedmodels

│		├──	__init__.py

│		└──	headmodel.py

│	└──	retrainedmodels


...

└── data

│	└──	raw_data

│	└──	processed_data

│		└──	__init__.py

│		└──	autodocsmodels.py

│	└──	user_input_data

...

```

Since the above are modules, each folder being accessed must have an __init__.py file within it.

### Cleaning Human Input Data

This isn't needed for this project - however we now have a better overview of the project structure.

# Writing Automated Documents

### autodocwriter.py

This file can contain a couple methods:

* Method that will write an "autodoc y" and associate it with "document x" every time a new document, "document x" is created.
* Method taht will update "autodoc y" whenever "autodoc x" is created.

For now, we will have the autodoc write, "hello world" for a new document and, "updated" once the document is edited.

This module should be callable from our routes.py.

newautodoc method Procedure:

1. Sponsor goes to @sponsor_bp.route('/sponsor/newdocument', methods=['GET','POST'])
2. New document is created in routes.py
3. Extract new document_id in routes.py
4. Pass new document_id in routes.py to the newautodocwrite() function
5. newautodocwrite() function 

We write up a function and import this as a module within routes.py.

```
(this function is similar to the function within routes.py for creating new documents and retentions.)
```

However, upon attempting to run the localhost url, we get an error: "sqlalchemy.exc.NoForeignKeysError."  This is likely because we didn't provide the proper ForeignKey relationship in either the models.py or autodocmodels.py.

The result was that the  "db.ForeignKey('autodocs.id')," had the wrong foreignkey, documents.id rather than autodocs.id.

### Testing if Working Properly

In order to test if woring properly, it's necessary to first create an admin user, and then a sponsor user and editor user.

Eventually, every time we do a restart, this is going to take a lot of work because the database doesn't persist.

Looking at the autodocs table via postgres, we see:

```
userlevels_flask_dev=# select * from autodocs;                                                                                                                  
 id |     body     | created_on                                                                                                                                 
----+--------------+------------                                                                                                                                
  1 | Hello World. |
```
Double checking to ensure that the revision helper table was updated as well:

```
userlevels_flask_dev=# select * from revisions;                                                                                                                 
 id | document_id | autodoc_id                                                                                                                                  
----+-------------+------------                                                                                                                                 
  1 |           1 |          1 
```
So to start off with, it's working fine.

### Displaying Autodocs on Sponsor View Route

So now that we have autodocs being created, we can modify our views, perhaps including our list views to display the result of the autodoc.

#### Sponsor Documents List View

Part of what we had learned working on views is that it's much more managable to create a single object to repesent everything in the display table that needs to be displayed at one time, basically create an SQL query with a join condition and then display that object, rather than try to combine multiple different queries.

So to start off with, our entire document list is as follows:

```
    # get document objects filtered by the current user
    document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).\
    join(Retention, User.id==Retention.editor_id).\
    join(Document, Document.id==Retention.document_id).\
    order_by(Retention.sponsor_id).\
    filter(Retention.sponsor_id == user_id)

```
The challenge is to not only include, "Document.document_name,Document.document_body" but also "Autodoc.body" for that document, based upon "Revision."

This would suggest:

* Join based upon Revision.document_id
* Autodoc.id called out by Revision for that Revision.document_id
* Display Autodoc.body

```
    # get document objects filtered by the current user
    document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).\
    join(Retention, User.id==Retention.editor_id).\
    join(Document, Document.id==Retention.document_id).\
    join(Document, Document.id==Revision.document_id).\
    order_by(Retention.sponsor_id).\
    filter(Retention.sponsor_id == user_id)

```
In order to be able to add, "Revision" and, "Autodoc" to the flask shell, we have to make sure that these classes are showing up in the flask shell environment via the context processor.

```
from project.static.data.processeddata.autodocsmodels import Autodoc, Revision

...

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention, 'Autodoc': Autodoc,'Revision': Revision}

```
After adding the above, we get on the flask shell:

```
>>> Revision                                                                                                           
<class 'project.static.data.processeddata.autodocsmodels.Revision'>                                                    
>>> Autodoc                                                                                                            
<class 'project.static.data.processeddata.autodocsmodels.Autodoc'> 
```
Running queries:

```
document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).order_by(Retention.sponsor_id).filter(Retention.sponsor_id == user_id)
```
At first there was some error running the query, which required a database restart.

```
document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body,Autodoc.body).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).order_by(Retention.sponsor_id).filter(Retention.sponsor_id == user_id).join(Revision,Revision.document_id==Document.id).join(Autodoc,Autodoc.id==Revision.autodoc_id)
```
In theory, the above should lock the Revision.document_id to the Document.id and the Autodoc.id to the Revision.autodoc_id, keeping the right autodocs attached to the right documents permanently.

When we try to create a new document, we get an error that, "Autodoc" is not defined. This is simply because we need to import it into routes.py.

Once this query works, we can then work with "documents" as a document object on the view including our autodoc, since it is already passing to the view with our render function:

```
    return render_template(
        'documentlist_sponsor.jinja2',
        documents=documents,
    )
```
Something I noticed while putting all of the above code together is that when passing to the view, the term, "body" is ambigious, because it all becomes, "document.(item)" and if "item" is "body" rather than "document_body" or "autodoc_body" it will become untenable if both are called, "body" rather than explicitly "thing_body."  So, I changed all Autodoc.body references to "Autodoc.autodoc_body".

#### Sponsor Individual Documents

Once the list view is working, it may be helpful to look at adding this functionality to the actual individual document view.

Needs Work

#### Editor View

Needs Work

#### Editor Individual Document View

Needs Work

# Installing Pre-Trained Model(s) Into the Environment

### A Word on Architecture

As mentioned previously in this readme, a more advanced version of prorgamming an app that leverages a pre-trained model, particularly a pre-trained model which uses neural networks, might be to create an additional volume within Docker and have that volume work only within the context of the GPU when calling certain functions.  Of course this depends upon what kind of cloud architecture is being used and how it is being charged.

For now, I'm just writing everything into the same monolithic app.

### Installing The Necessary Components

To be added to requirements.txt:

```
gast==0.4.0
```
* [GAST](https://pypi.org/project/gast/) is a generic AST to represent Python2 and Python3’s Abstract Syntax Tree(AST).

```
transformers==4.5.1
```
* [Transformers](https://pypi.org/project/transformers/)

After installing these two packages, the image size is now 299MB up from 175MB.

There may be a way to make this image size smaller by only importing specific modules from within, "transformers" -

```
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

```

# Running Tokenizer

### Encoding Context - GPT2Tokenizer - doctokenization.py

The first step in tokenizing is to import our GPT2Tokenizer.

```
from transformers import GPT2Tokenizer
```

GPT2 has its own encoding and tokenization system which takes raw text as an input. Presumably, all of the necessary regex is already built into the system.

```
# encode context the generation is conditioned on
input_ids = tokenizer.encode('We have a lot of new SOCs in stock', return_tensors='tf')
```
To define which document we are going to tokenize, we need an document_id, with which we can look up our autodoc id and then write a completely automated text based upon our document body.

```
def gpt2tokenize(document_id):
```
From there we can run the text generator by calling a seperate function to autodocwriter.py.

# Utilizing the MLModel

### Envoking vs. Training

The ML model can be envoked in /mlmodels/seedmlmodels as GPT2 already exists as a is pre-built by OpenAI, we are merely envoking it.

```
mlmodel = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
```
### Envoking via headmodel.py


# Prediction / Text Generation

### The GPT2 Prediction - model.generate

The prediction essentially happens in the following line:

```
# set no_repeat_ngram_size to 4
beam_output = model.generate(
    input_ids, 
    max_length=100, 
    num_beams=5, 
    no_repeat_ngram_size=4, 
    early_stopping=True
)

print("Output:\n" + 100 * '-')
print(tokenizer.decode(beam_output[0], skip_special_tokens=True))
```

# Splitting Training and Test Set in Source Code

This project does not include training, since we're using an already pre-trained model produced by GPT2.

# Fitting Model with Training Data


This project iteration does not include fitting, since we're using an already pre-trained model produced by GPT2.

# "Pickle" the Model (Or Download the Model)

Again, there is nothing within this repo which involvse training, so nothing is needed here.

# Request.py File for File

In this prjoect, there isn't a CSV being uploaded with data, it's not a linear regression type problem, so there is no need for any request.py file, basically it's already built-in.

# Example Source CSV File

In this project, there is no need for a CSV upload as discussed above.

# Jsonify Output

# Conclusion

# Future Work

# Resources

* [Deploy Machine Learning Model with Flask ](https://www.analyticsvidhya.com/blog/2020/04/how-to-deploy-machine-learning-model-flask/)...based upon Twitter Sentiment analysis.
* [Integrating Machine Learning Applications with Flask](https://www.analyticsvidhya.com/blog/2020/09/integrating-machine-learning-into-web-applications-with-flask/)
* [How to Easily Deploy Machine Learning Models Using Flask](https://towardsdatascience.com/how-to-easily-deploy-machine-learning-models-using-flask-b95af8fe34d4)