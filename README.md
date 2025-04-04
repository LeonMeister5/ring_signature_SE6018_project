# Ring_Signature_SE6018_project
This is an implementation of 3 participant ring signature, whose diagram is on my notebook p9. 

All parameters in this project is int. So my matrix number is transformed into int. 

The submission of source file is ring_signature.ipynb. 

The not_used.py is not part of the project. It's something I wrote but later found useless. I don't want to delete it. 

This is SE6018 final project. I put it public for employers to see. Students please don't copy. 

# Don't run rsa_generation.ipynb
rsa_generation.ipynb generates 3 sets of RSA parameters for the users, storing them in user1_key.txt, user2_key.txt and user3_key.txt. 

RSA user generation is in rsa.py. Since I have to calculate x2, the other 2 users can not be generated randomly every time.

Therefore the 3 user's RSA parameters is generated before the running ring_signature.ipynb. Then I can calculate x2, and use it in ring_signature.ipynb. 

# useri_keys.txt
As is required, d is not inside. I have to calculate d myself in ring_signature.ipynb. I think it's better to store d inside it too. 

# calculate_x2.ipynb
That's how I calculate x2 based on the 3 users. The result will be stored in x2.txt. 

# ring_signature.ipynb
This is the ring_signature and verification part. 

# What you should do to judge my project
Don't run rsa_generation.ipynb. Just read through it. Running it will cause rewriting 3 txt files. If you insist on that, it's okay. x2 will be changed and result will still be correct. 

You should run ring_signature.ipynb and check result. 

You should run calculate_x2.ipynb and check x2. 

My version of python is python 13.2.0.
