# $1 is driver, $2 is application
rm -rf build
cp -r frame build
cp -r $1/* build
cp -r $2/* build

# state machine generation
export PYTHONDONTWRITEBYTECODE=1
cp buildtools/chart.py build/
cd build
python3 chart.py &&
dot -Tsvg graph.dot > ../output/state_machine.svg &&
convert -density 600 ../output/state_machine.svg ../output/state_machine.png &&
rm graph.dot
rm chart.py

# extraneous file removal
find . -type d -name __pycache__ -exec rm -r {} \+
rm README.md
cd - 
