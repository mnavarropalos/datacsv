# datacsv

## Requirements
This scripts only supports Python 2.7

### Input data format -- Input file (Example)

id: Pollito
color: Amarillo
edad: 4
skill: Volador

id: Tortuga
skill: Agua

## Output data format -- Output file (Example)

skill_0,id_0,color_0,edad_0
Volador,Pollito,Amarillo,4
Agua,Tortuga,,


## Usage

    $ python datacsv.py -i [input file] -o [output file]

