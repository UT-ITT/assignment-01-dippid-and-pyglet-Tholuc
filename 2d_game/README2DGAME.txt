Dear tutors again,

I wanted to keep it simple for my sake but try to structure it well and give u a fun fantasy.
So i made a simple collect the dot game but included dog cat mouse as i think that is a fantasy everyone gets. 
My partner actually had the idea to include a chase dog and i think thats has been very good since i can have a game over screen/reset that felt natural and was lacking beforehand. We also had fun making the sounds. 
I hope they dont make any trouble for ur testing workflow. When testing in python i had no problems and when using visual studio i had to use:

import os
os.chdir(os.path.dirname(__file__)) # this fixed an issue for testing in Visual Studio Code with Sounds 

to force the python file beeing used in the directory where i had the sound files. VS does some weird stuff otherwise.

Designwise i kept things light. Thats why i made the characters out of the pyglet shapes instead of images. Also i used the create functions for moving instead of like moving the pieces. This way it is less code but more inefficient. For such a small prototype i thought that is okay. 
Also i kept in the magic numbers i did not play with i hope thats okay. Otherwise i think it would have gotten less readable again. Like the Colors and size of the my animals was kinda set and i didnt really wanna play around with it and the extra variables would have added unnecessary complexity.

For game feel i made that the dog became faster the higher score you got so a high score is actually hard to get.

Oh also i used the accelerator as that kinda felt better for me and with my phone. I dont know if that differs on another setup. 

And then i did a highscore that works for the session. Thought highscore that reads data would have been overkill but like this u can atleast play to a personal highscore :)

My highscore with the last setup was 36 :^)

