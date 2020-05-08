import setuptools                                                                                                                        

with open ("README.md", "r") as fh: 
     long_description = fh.read() 

setuptools.setup( 
     name="universal-realtime-noro", 
     version="0.0.1", 
     author="JvLS_DK", 
     author_email="danielkim478@gmail.com", 
     description="FAES Python Final Project", 
     long_description=long_description, 
     long_description_content_type="text/markdown", 
     url="https://github.com/JessvLS/project_spring_2020.git", 
     packages=setuptools.find_packages(), 
     classifiers=[ 
         "Programming Language :: Python :: 3", 
         "License :: Apache License", 
         "Operating System :: OS Independent", 
     ], 
     python_requires='>=3.6', 
)

