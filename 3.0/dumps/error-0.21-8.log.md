Oops! Sol just crashed;
Here's this crash log!

Quick Fix for users: N/A (Not Available)

Cause: None
Context: SoundSystem.play() got an unexpected keyword argument 'cc'
Exceptions (if available): None
Error Type: TypeError
Error: SoundSystem.play() got an unexpected keyword argument 'cc'

FrameSummary #1:
  | Filename: D:\Code\Eklips\3.0\Sol.py
  | Line: ux.blit(resld.render(data["Lang"]["munk1"]), [50,250], alpha=2)
  | Line #: 267
  | Data: None

FrameSummary #2:
  | Filename: D:\Code\Eklips\3.0\classes\ui.py
  | Line: self.sfx.play(self.clk, cc="click.mp3")
  | Line #: 408
  | Data: None

Traceback dictionary: {'max_group_width': 15, 'max_group_depth': 10, 'stack': [<FrameSummary file D:\Code\Eklips\3.0\Sol.py, line 267 in <module>>, <FrameSummary file D:\Code\Eklips\3.0\classes\ui.py, line 408 in blit>], '_exc_type': <class 'TypeError'>, '_str': "SoundSystem.play() got an unexpected keyword argument 'cc'", '__notes__': None, '_is_syntax_error': False, '_have_exc_type': True, 'exc_type_qualname': 'TypeError', 'exc_type_module': 'builtins', '__suppress_context__': False, '__cause__': None, '__context__': <traceback.TracebackException object at 0x000001ABD88BCB90>, 'exceptions': None}


Please send this file to the developers of Sol at https://github.com/Za9-118/Sol/issues.
Your feedback is important to me!