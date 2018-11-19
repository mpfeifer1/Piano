# PIANO Is Anyone's Next Overture
Create your next overture using Piano!

Piano is designed to allow composers to programmatically and efficiently create songs in midi files. 

### Dependencies
Piano uses the Lark Parser and Mido for Python.  These are needed to run Piano.  These can be installed using pip.

    $ pip install lark-parser
    $ pip install lark
    $ pip install mido

### Compile Code
This is the current way of running a file and will be updated in the future as the project progresses.  
The *piano.py* file is located under the src directory.

    $ ./piano.py -p example.pno -m example.midi

### Running Tests
The Continuous Integration (CI) hook is set up by running the following.

    $ ./scripts/install-hooks.bash
This hook will create a pre-commit call to the run tests file (run-tests.bash) everytime that a commit is attempted.  
This hook is **REQUIRED** if you wish to contribute to our project.

The file to run the tests is called *run-tests.bash* and it is located in the scripts directory.
This script will run the available test files.
All tests should be passing before and after any code is pushed.  If all tests are not, a description of the error will be outputted.

    $ ./scripts/run-tests.bash
Or a given test can be run using python.

    $ python semantictest.py
    
### Example Files

```
// Mary Had A Little Lamb
$V = violin
Compose {
	timesig(2/4)
	tempo(100)
	Measure {
		$V {1/8 E4; 1/8 D4; 1/8 C4; 1/8 D4; }
	}
	Measure {
		$V {1/8 E4; 1/8 E4; 1/4 E4; }
	}
	Measure {
		$V {1/8 D4; 1/8 D4; 1/4 D4; }
	}
	Measure {
		$V {1/8 E4; 1/8 G4; 1/4 G4; }
	}
	Measure {
		$V {1/8 E4; 1/8 D4; 1/8 C4; 1/8 D4; }
	}
	Measure {
		$V {1/8 E4; 1/8 E4; 1/8 E4; 1/8 E4; }
	}
	Measure {
		$V {1/8 D4; 1/8 D4; 1/8 E4; 1/8 D4; }
	}
	Measure {
		$V {1/2 C4;}
	}
}
```
