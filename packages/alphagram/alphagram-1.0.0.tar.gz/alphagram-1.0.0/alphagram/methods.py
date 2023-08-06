from pyrogram import *

class Alpha(Client):
  def __init__(self,
               name,
               api_id=13691707, 
               api_hash="2a31b117896c5c7da27c74025aa602b8",
               bot_token=None,
               session_string=None,
               plugins={}
              ):
    super().__init__(f'{name}-alphagram',
                     api_id=api_id,
                     api_hash=api_hash,
                     bot_token=bot_token,
                     session_string=session_string,
                     plugins=plugins
                    )
    
  def start(self, to_print: str = None):
    if not to_print:
      to_print = f'[{self.name}]'
    print(to_print)  
    super().start()
    self.me = self.get_me()
