from transformers import GPT2Tokenizer

# import documents model
# import models
from project.models import db, Document


def gpt2tokenize(document_id):

	# look up the document text
	document_body = db.session.query(Document).filter_by(id = document_id)[0].document_body

	# encode context the generation is conditioned on
	# tokenize document_body
	input_ids = tokenizer.encode(document_body, return_tensors='tf')

	# call the text autocodewriter function
	return(input_ids)
