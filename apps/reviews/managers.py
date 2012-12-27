# django imports
from django.db import models

class ActiveManager(models.Manager):
    """An extended manager to return active objects.
    """
    def active(self):
        return super(ActiveManager, self).get_query_set().filter(active=True)
   

class VoteManager(models.Manager):  
	def active(self):
		return super(VoteManager, self).get_query_set().filter(active=True)

	def type_1_count(self):
		return super(VoteManager, self).get_query_set().filter(vote_type=1, active=True).count()

	def type_2_count(self):
		return super(VoteManager, self).get_query_set().filter(vote_type=2,active=True).count()
		
