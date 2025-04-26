# Ring_Signature_SE6018_project
My python version is 3.12.0.

I do this on windows10 laptop. \n and \r\n issue may matter. 

This is an implementation of 3 participant ring signature, whose diagram is on my notebook p9. 

This is SE6018 final project. I put it public for employers to see. Students please don't copy. 

# Special notice
Padding 0 in the front is really f****** import. m > n in rsa will lead to fatal error. This issue stop me from sleeping til 3am. 

# rsa_generation.py
Generate 3 users' N, p, q, d, e, rewrite into 3 txt files. In the latest version, I fixed rsa generation failure issue. I check whether the p, q, e pairs is valid by perfoming ring signature, and regenerate when it fails. So the ring signature will be always valid. This makes generating speed 1.5 times slower, but 100% correct. 

# calculate_x2.py
Calculate x2, given 3 users' RSA keys. 

# ring_signature.py
Implementation and verification of ring signature. It works based on the calculated x2. 

# not_used.py.txt
Some not used codes. I don't want to delete, and I don't know where to keep it. So I throw it here. 

# What you should do to judge my project 1
You can do manually. 

python rsa_generation.py

python calculate_x2.py

python ring_signature.py

Sequence matters. By running these 3 source files, you generate 3 sets of RSA keys, calculate x2 and use my matrix number to do ring signature. 

# What you should do to judge my project 2
You can also use check_project.ipynb. It is equivalent to running 3 commands and check for 100 times.
