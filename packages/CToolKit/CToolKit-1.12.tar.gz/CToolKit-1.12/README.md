# CToolkit
 is An Python Package to manipulate C/C++ buildings and  PipeLines
 providing easy automation tools to increase your code pipelines 
 with amalgamations, black box testing, and readme replacment

### Instalation from Pip
for install the lib from pip call 

~~~shell
pip install CToolKit
~~~
### Installation from scratch

clone the repo into your machine with:

~~~shell
git clone https://github.com/OUIsolutions/CTolkitBuild.git
~~~
Then install with:
~~~shell
cd CTolkitBuild/
pip install .
~~~

### Installation from github
type the following comand to install from github
~~~shell
pip install git+https://github.com/OUIsolutions/CTolkitBuild.git
~~~

### Amalgamation System

for amalgamate an C lib its super easy, just call 
~~~python
import CToolKit as ct

STARTER  = f'test.h'
OUTPUT = 'amalgamated.h'
amalgamated_code = ct.generate_amalgamated_code(STARTER)
with open(OUTPUT,'w') as arq:
    arq.write(amalgamated_code)
~~~
or even more implicit:
~~~python

import CToolKit as ct

STARTER  = f'CTextEngine/CTextEngineMain.h'
OUTPUT = 'amalgamated.h'
amalgamated_code = ct.generate_amalgamated_code(STARTER,OUTPUT)

~~~

### Comand Line Operations

#### Compile an Project 
it wil copile the given file

~~~python


import CToolKit as ct

COMPILER = 'gcc'
FILE = 'test.c'
OUTPUT = 'test.out'
ct.compile_project(
 COMPILER,
 FILE,
 OUTPUT,
 raise_errors=True,
 raise_warnings=True
)
~~~

#### Testing copilation with valgrind 

Execute an valgrind testing of the given binary ( you need to have valgrind installed in your os)

~~~python
import CToolKit as ct

COMPILER = 'gcc'
FILE = 'test.c'
OUTPUT = 'test.out'
ct.compile_project(
 COMPILER,
 FILE,
 OUTPUT,
 raise_errors=True,
 raise_warnings=True
)

FLAGS = ['-libcur']
ct.test_binary_with_valgrind(OUTPUT, FLAGS)
~~~
Executing copilation and test with file with a single comand 
~~~python
import CToolKit as ct

COMPILER = 'gcc'
FILE = 'test.c'

ct.execute_test_for_file(COMPILER,FILE)

~~~

Executing Test with all .c or .cpp files in the given folder 

~~~python 

import CToolKit as ct

COMPILER = 'gcc'
FOLDER ='test'
ct.execute_test_for_folder(COMPILER,FOLDER,print_values=True)

~~~

#### Execution 
you can execute an binary with the ComandLine Execution class

~~~python

import CToolKit as ct

COMPILER = 'gcc'

FILE = 'test.c'
OUTPUT = 'test.out'
ct.compile_project(
 COMPILER,
 FILE,
 OUTPUT,
 raise_errors=True,
 raise_warnings=True
)

execution = ct.ComandLineExecution(f'./{OUTPUT}')

print('output:', execution.output)
print('statuscode:', execution.status_code)
~~~
#### Readme Replacement 
you can replace readme content with code system 
for these just tipe: < + !--codeof:test.c-->, you can see 
these example in the following lib:
https://github.com/OUIsolutions/CTextEngine

~~~Markdown
Will free the memory
<!--codeof:exemples/free.c-->
~~~
~~~python

import CToolKit as ct

ct.include_code_in_markdown('README.md')
~~~






