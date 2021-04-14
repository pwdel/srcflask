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

```

```


# Picking a Model to Work With

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