import os
os.chdir(r'c:\Users\maryl\wastedash--main')
from streamlit.testing.v1 import AppTest

at = AppTest.from_file(r'c:\Users\maryl\wastedash--main\app.py', default_timeout=30).run()
assert not at.exception, at.exception
at.session_state.current_page = 'Auth'
at.run()
assert not at.exception, at.exception

# Customer Login tab with collector credentials -> must be rejected
fm = {f.key: f for f in at.get('form')} if hasattr(at, 'get') else {}
ti = at.text_input
ti[0].set_value('priya@wastedash.in'); ti[1].set_value('wastedash123')
at.button[0].click().run()  # first form submit in customer login
print('errors:', [e.value for e in at.error])
print('user_id:', at.session_state.user_id)

# Collector Login radio
at.radio[0].set_value('Collector Login').run()
ti = at.text_input
ti[0].set_value('priya@wastedash.in'); ti[1].set_value('wastedash123')
at.button[0].click().run()
print('after collector login user_id:', at.session_state.user_id, 'page:', at.session_state.current_page)
print('buttons:', [b.label for b in at.button])
assert not at.exception, at.exception
