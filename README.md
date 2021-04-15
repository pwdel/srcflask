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

│	└──	retrained_models

└── data

│	└──	raw_data

│	└──	processed_data

│	└──	user_input_data

└── pipeline

│	└──	model_retraining_automation_scripts

└── docs

	└──	Documentation

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


# Cleaning Data in Source Code

# Splitting Training and Test Set in Source Code

# Fitting Model with Training Data

# Pickle the Model

# Request.py File for File

# Example Source CSV File

# Route for Prediction

# Jsonify Output

# Upload Custom CSV File

# Resources

* [Deploy Machine Learning Model with Flask ](https://www.analyticsvidhya.com/blog/2020/04/how-to-deploy-machine-learning-model-flask/)...based upon Twitter Sentiment analysis.
* [Integrating Machine Learning Applications with Flask](https://www.analyticsvidhya.com/blog/2020/09/integrating-machine-learning-into-web-applications-with-flask/)
* [How to Easily Deploy Machine Learning Models Using Flask](https://towardsdatascience.com/how-to-easily-deploy-machine-learning-models-using-flask-b95af8fe34d4)