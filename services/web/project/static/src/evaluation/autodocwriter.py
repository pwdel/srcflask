# import the database
from project import db
# import the transformers GPT2 head model
from transformers import TFGPT2LMHeadModel
# import tokenizer
from transformers import GPT2Tokenizer


# import the autodocs models class
# import autodocsmodels.py
from project.static.data.processeddata import autodocsmodels
from project.static.data.processeddata.autodocsmodels import Autodoc, Revision

def autodocwrite(document_id,input_ids):

	# set GPT2 tokenizer
	tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

	# set model
	model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

	# autogenerate based upon input_ids
	# set no_repeat_ngram_size to 4
	# generate model
	beam_output = model.generate(
	    input_ids, 
	    max_length=100, 
	    num_beams=5, 
	    no_repeat_ngram_size=4, 
	    early_stopping=True
	)

	# decode and write text with tokenizer
	autodoc_body = tokenizer.decode(beam_output[0], skip_special_tokens=True)

	# create a new autodoc entry
	autodoc = Autodoc(
		autodoc_body=autodoc_body
		)
        
    # add retention to session and commit to database
	db.session.add(autodoc)
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
	autodoc_id = last_autodoc.id


	# create a new retention entry
	newrevision = Revision(
		document_id=document_id,
		autodoc_id=autodoc_id
		)
        
    # add retention to session and commit to database
	db.session.add(newrevision)
	db.session.commit()