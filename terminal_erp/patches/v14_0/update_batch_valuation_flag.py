import terminal_framework


def execute():
	"""
	- Don't use batchwise valuation for existing batches.
	- Only batches created after this patch shoule use it.
	"""

	batch = terminal_framework.qb.DocType("Batch")
	terminal_framework.qb.update(batch).set(batch.use_batchwise_valuation, 0).run()
