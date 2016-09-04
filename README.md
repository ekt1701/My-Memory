# My-Memory
When did I? Where did I put it? How long until?

I wanted a simple way to remember things using Alexa.  The skill uses a csv file hosted somewhere, to hold the information to be remembered. Personally, I saved the csv file in DropBox, which can easily be edited with a text editor. (Note when you get the link from DropBox change ?dl=0 to ?raw=1) The format is "keyword,description,date" (Note: date has to be in the format mm/dd/yyyy)

The code currently links to the sample myMemory.csv file hosted here on GitHub

You are not limited to three fields, you can customize it and adjust the code accordingly.

The configuration is Runtime: Python 2.7, Handler: lambda_function.lambda_handler, Existing Role: lambda_basic_execution. The code is entered in-line. You will need to create a Custom Slot with the name ANSWERS and add words and phrases in the Value section, that you would use.




