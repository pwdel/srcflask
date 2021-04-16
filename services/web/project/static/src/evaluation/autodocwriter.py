# import the database
from project import db
# import the autodocs models class

# import autodocsmodels.py
from project.static.data.processeddata import autodocsmodels
from project.static.data.processeddata.autodocsmodels import Autodoc, Revision

def newautodocwrite(newdocument_id):
	# create a new autodoc entry
	newautodoc = Autodoc(
		autodoc_body='Hello World.'
		)
        
    # add retention to session and commit to database
	db.session.add(newautodoc)
	db.session.commit()

    # find new autodoc id number
    # after this autodoc has just been added to the database, add revision
    # query all autodocs in order, put into a python object
	all_autodocs_ordered = Autodoc.query.order_by(Autodoc.id)
    # query count of all autodocs, subtract 1 because python index starts at 0
	autodoc_index = Autodoc.query.count() - 1
    # last autodoc object is autodoc index, or count-1
	last_autodoc = all_autodocs_ordered[autodoc_index]
    # new autodoc id for retentions database is indexed last autodocid integer
	newautodoc_id = last_autodoc.id


	# create a new retention entry
	newrevision = Revision(
		document_id=newdocument_id,
		autodoc_id=newautodoc_id
		)
        
    # add retention to session and commit to database
	db.session.add(newrevision)
	db.session.commit()