import tkinter
import traceback, os
import webbrowser
from tkinter import ttk
from tkinter.messagebox import *

ErrorData = 0

class Preview(Exception): #Preview Error Class
	def __none__(self): return None

def raise_error(vers, ISTRACEBACK,runninge): #Raise error
	global ErrorData
	running=""
	for i in runninge:
		running=i+", "
	print(f"GetErrorStats({vers}, {ISTRACEBACK})")
	if ISTRACEBACK:
		ErrorObject=traceback.TracebackException.from_exception(ErrorData)
		ErrorInfo=f"""Cause: {ErrorObject.__cause__}
Context: {ErrorObject.__context__}
Exceptions (if available): {ErrorObject.exceptions}
Error Type: {ErrorObject.exc_type_str}
Error: {ErrorObject}
"""
	
		fsid=1
		for i in ErrorObject.stack:
			ErrorInfo+=f"""
FrameSummary #{fsid}:
  | Filename: {i.filename}
  | Line: {i.line}
  | Line #: {i.lineno}
  | Data: {i.locals}
"""
			fsid+=1
	
		try:
			ErrorInfo+=f"""SyntaxError related:
  | Filename: {ErrorObject.filename}
  | Message: {ErrorObject.msg}
  | Offset: {ErrorObject.offset}
  | EndOffset: {ErrorObject.end_offset}
  | Text: {ErrorObject.text}
  | Line#: {ErrorObject.lineno}
  | End Line#: {ErrorObject.end_lineno}
"""
		except:
			pass
		ErrorInfo+=f"""
Traceback dictionary: {ErrorObject.__dict__}
"""
		try:
			os.mkdir("dumps")
		except:
			pass
		fn=f"dumps/error-{vers}-{len(os.listdir('dumps'))+1}.log.md"
	
		QuickFix = "N/A (Not Available)"
		if ErrorObject.exc_type_str == "Preview":
			QuickFix = "The Eklips Error handler recieved no data, so you got this error."
		elif (ErrorObject.exc_type_str == "pygame.error" and ErrorObject == "Out of memory") or ErrorObject.exc_type_str == "MemoryError":
			QuickFix = "Eklips ran out of memory! Try giving the app more memory to work with."
		elif ErrorObject.exc_type_str in ["ImportError", "ModuleNotFoundError"]:
			QuickFix = "Core Eklips Modules were removed/not found, try reinstalling them through Eklips' github repo."
		elif ErrorObject.exc_type_str == "KeyboardInterrupt":
			QuickFix = "You pressed Ctrl+C/Delete. Don't do that next time okay?"
	else:
		fn=f"dumps/error-{vers}-{len(os.listdir('dumps'))+1}.log.md"
		QuickFix="N/A (Not Available)"
		ErrorInfo=f"The Traceback data could not be found. Attached value: {ErrorData}"
	with open(fn, "w") as f:
		f.write("Oops! Eklips just crashed;\nHere's this crash log!\n\n")
		f.write(f"Quick Fix for users: {QuickFix}\nRunning applications: {running}\n\n")
		f.write(ErrorInfo)
		f.write("\n\nPlease send this file to the developers of Eklips at https://github.com/Za9-118/Eklips/issues. \nYour feedback is important!")
	print("rs;DoneStats\nrs;ask")
	answer=askyesno(f"Eklips v{vers}", f"Quick fix for users: {QuickFix}\nRunning applications: {running}\n\n{ErrorInfo}\n\nWould you like to send a bug report?")
	print("rs;answer")
	if answer:
		webbrowser.open_new_tab("https://github.com/Za9-118/Eklips/issues/new/choose")
	else:
		pass

def error(version, error, running, ISTRACEBACK=1):
	global ErrorData
	
	ErrorData = error
	print(f"ErrorData=>error (error={error})")
	raise_error(version, ISTRACEBACK, running)

if __name__ == "__main__":
	error("", MemoryError("This is not an error, this is a preview"))
