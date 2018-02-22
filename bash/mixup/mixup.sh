#/bin/bash
echo "Hi who! Very nice to meet you!"
cat ~/.bashrc > ~/.fakerc
echo "alias whoami='echo \"You are who! Do you not remember?!\"'" >> ~/.fakerc
bash --rcfile <(echo ". ~/.fakerc; rm ~/.fakerc")
