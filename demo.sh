#!/bin/bash

echo "Running the medical enhancement pipeline for image images/001.tif..."
python app.py -i images/001.tif --log-gain 4.0 --clip-limit 2.5 --tile-grid-size 8 --unsharp-amount 0.6
echo "Done!"
