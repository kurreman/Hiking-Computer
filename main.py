from SIGFOX import setup_sigfox
from data_gathering import gather_data

#SIGFOX SETUP
s = setup_sigfox()
#Data gathering
gather_data(s)