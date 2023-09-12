
import frappe 

def autoname(self,method):
    if self.short_name:
        self.name = self.short_name.title()
    
