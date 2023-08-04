# # from distutils.sysconfig import get_python_lib; print(get_python_lib()) 
import NLP
import requests
import threading
import time
# input_data = input()
# user_input = NLP.response(input_data)
#     # response2 = requests.post('http://localhost:5000/get_data', data={'output': user_input})
# print("User input:", user_input) # print the user input
#     # sp(user_input)
# # name.set(user_input) # clear the name variable
#     # input1.set(user_input)
#     # animate_text(user_input, 100)

def update():
  
  response1 = requests.get('http://localhost:5000/send_sent_data')
  # print(response1.text)
  input_data = response1.text
  user_input = NLP.response(input_data)  #################################################################
  response2 = requests.post('http://localhost:5000/get_data', data={'output': user_input})
  # print("User input:", user_input) # print the user input
  time.sleep(1)
    # sp(user_input)
    # name.set(user_input) # clear the name variable
    # input1.set(user_input)
    # animate_text(user_input, 100)
  # if user_input == input_data:
  #       event = threading.Event()
  #       event.wait(1) # wait for 0.1 seconds before continuing with your code
  # else:
  return response2.text, user_input
  
    
    

# animate_text(user_input,100)
    
while True:
 if update() == update():
         event = threading.Event()
         event.wait(1) # wait for 0.1 seconds before continuing with your code

  
 else:
   update()
        

