#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests, zipfile, io
r = requests.get('http://web.mta.info/developers/data/nyct/subway/google_transit.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

