# This is an ADIF parser in Python.

## Actual usage

Main result of parsing: List of QSOs:

* Each QSO is represented by a special-purpose Python mapping.
* Keys in that mapping are ADIF field names in upper case,
* value for a key is whatever was found in the ADIF, as a string
  (though some values are converted to upper case on output),
* you can access individual field values via either 
  `qso[fieldname]` or [`qso.get(fieldname)`](https://docs.python.org/3/library/stdtypes.html#dict.get)
  (depending on which behavior you want when your field does not exist).

Order of QSOs in the list is same as in ADIF file.

Secondary result of parsing: The ADIF headers.
This is returned as a Python mapping as well.

Normally, you'd call `adif_io.read_from_file(filename)`.  But you can
also provide a string with an ADI-file's content, as follows:

```
import adif_io

qsos, header =  adif_io.read_from_string(
    "A sample ADIF content for demonstration.\n"
    "<adif_ver:5>3.1.0<eoh>\n"
    
    "<QSO_DATE:8>20190714 <time_on:4>1140<CALL:5>LY0HQ"
    "<mode:2>CW<BAND:3>40M<RST_SENT:3>599<RST_RCVD:3>599"
    "<STX_STRING:2>28<SRX_STRING:4>LRMD<EOR>\n"

    "<QSO_DATE:8>20190714<TIME_ON:4>1130<CALL:5>SE9HQ<MODE:2>CW<FREQ:1>7"
    "<BAND:3>40M<RST_SENT:3>599<RST_RCVD:3>599"
    "<SRX_STRING:3>SSA<DXCC:3>284<EOR>")
```

After this setup, `print(header)` will print out a valid ADIF file start:

>  &lt;ADIF_VER:5>3.1.0 &lt;EOH>

(This starts with a blank space, as the ADIF spec demands a header must not
start with the `<` character.)

And 

```
for qso in qsos:
    print(qso)
```

prints

> &lt;QSO_DATE:8>20190714 &lt;TIME_ON:4>1140 &lt;CALL:5>LY0HQ &lt;MODE:2>CW &lt;BAND:3>40M &lt;RST_RCVD:3>599 &lt;RST_SENT:3>599 &lt;SRX_STRING:4>LRMD &lt;STX_STRING:2>28 &lt;EOR>
> 
> &lt;QSO_DATE:8>20190714 &lt;TIME_ON:4>1130 &lt;CALL:5>SE9HQ &lt;FREQ:1>7 &lt;MODE:2>CW &lt;BAND:3>40M &lt;DXCC:3>284 &lt;RST_RCVD:3>599 &lt;RST_SENT:3>599 &lt;SRX_STRING:3>SSA &lt;EOR>
> 

So `str(qso)` for a single QSO generates that QSO as an ADIF string.

Fine points:

- The ADIF string of the headers or that of a QSO are each terminated by a `\n`.
- ADIF allows lower- and upper case field names. You can feed either to this software.
- Field names are consistently converted to upper case internally.
- Any non-field text in the header or in a QSO or between QSOs is ignored.
  (This may change at some undetermined time in the future.)
- Value content is always a string.
- Fields with zero-length content are treated as non-existent.
- The output of a single QSO has a few important fields first, 
  then all other fields in alphabetic order.
  The details may change over time.
- Some QSO fields, in particular `CALL` and `MODE`, are automatically converted to upper case on output.
  This is not done systematically (for other fields that would also benefit from this),
  and the details may change.


## Time on and time off

Given one `qso` dict, you can also have the QSO's start time calculated as a Python `datetime.datetime` value:

    adif_io.time_on(qsos[0])

If your QSO data also includes `TIME_OFF` fields (and, ideally, though
not required, `QSO_DATE_OFF`), this will also work:

    adif_io.time_off(qsos[0])

## Geographic coordinates - to some degree

ADIF uses a somewhat peculiar 11 character `XDDD MM.MMM` format to
code geographic coordinates (fields `LAT` or `LON`).  The more common
format these days are simple floats that code degrees.  You can convert
from one to the other:

```
adif_io.degrees_from_location("N052 26.592") # Result: 52.4432
adif_io.location_from_degrees(52.4432, True) # Result: "N052 26.592"
```

The additional `bool` argument of `location_from_degrees` should be
`True` for latitudes (N / S) and `False` for longitudes (E / W).

## ADIF version

There is little ADIF-version-specific here.  (Everything should work
with ADI-files of ADIF version 3.1.3, if you want to nail it.)

## Not supported: ADIF data types.

This parser knows nothing about ADIF data types or enumerations.
Everything is a string. So in that sense, this parser is fairly simple.

But it does correcly handle things like:

    <notes:66>In this QSO, we discussed ADIF and in particular the <eor> marker.

So, in that sense, this parser is _somewhat_ sophisticated.

## Only ADI.

This parser only handles ADI files. It knows nothing of the ADX file format.

## Sample code

Here is some sample code:

```
import adif_io

qsos_raw, adif_header = adif_io.read_from_file("log.adi")

# The QSOs are probably sorted by QSO time already, but make sure:
qsos_raw_sorted = sorted(qsos_raw, key = adif_io.time_on)
```

Pandas / Jupyter users may want to add `import pandas as pd`
up above and continue like this:

```
qsos = pd.DataFrame(qsos_raw_sorted)
qsos.info()
```
