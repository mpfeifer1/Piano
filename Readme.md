# PIANO Is Anyone's Next Overture
Create your next overture using Piano!

Write songs in Piano to midi files!


### Dependencies
Piano uses the Lark Parser for Python.
Some other things are needed too.

    $ pip install lark-parser
    $ pip install lark
    $ pip install mido

### Compile Code
Current way of running a file.  This will be updated in the future.
    $ python piano.py -p example.pno -m example.midi

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

### Run Tests
The file to run the tests is called 'run-tests.bash' and it is located in the scripts directory.
This script will run the available test files, 'ourtests.py' and 'semantictests.py'.
All tests should be passing.  If all are not, a description of the error will be outputted.

    $ ./scripts/run-tests.bash
    
