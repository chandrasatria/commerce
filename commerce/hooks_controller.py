# ini ada karena anomali panggil xendit di doctype function g work

from commerce.doctype_function import *

def on_update_after_submit(self,method):
	import traceback
	from commerce.tools.error import error
	err_title = "Error Callback Xendit"
	err_message = traceback.format_exc()
	error(log_message=err_title, log_title=err_message, err_message=err_title, err_title=None, raise_exception=False)