

Installing PySDL2
1. Download:
   https://bitbucket.org/marcusva/py-sdl2/downloads/PySDL2-0.9.2.zip
2. Unzip
3. 'cd ~/Downloads/PySDL2-0.9.2'
4. 'python setup.py install' or 'make install'

Running
'python realtime.py'

Mouse Events
Click on the window and it will add a box size 0.25 x 0.25 x 0.25 to that point relative to the original coordinate system.
It will sometimes seem that the x-axis is reversed and this is because that it adds the box to the original coordinate system and not to the "varied" one.