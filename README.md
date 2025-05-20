Automata Manager Application
=========================
(code source : https://github.com/Yassinelouizi123/gestion-automates)
(executable : https://drive.google.com/file/d/1dIvowofUOuiNVf8nbJgeMkPaYlZ5Xn2h/view?usp=sharing  ) 
PS : if you run the .exe it might take 10 or so seconds as it creates the file to save automatons and the user.db
This application allows you to create, visualize, and analyze finite automata, including performing operations like union, intersection, and complement.

Setup Instructions
----------------
1. Make sure you have Python 3.7 or higher installed on your system.

2. Install the required dependencies by opening a terminal in this folder and running:
   pip install -r requirements.txt
   install Graphviz system tool from : https://graphviz.org/download/
   and then run pip install graphviz in your terminal


3. Run the application:
   python app.py

First Time Usage
--------------
1. When you first run the application, you'll be prompted to log in.

   Default credentials:

   - Admin account
     - Username: admin
     - Password: admin123

   - Normal user account
     - Username: user1
     - Password: 123456789

2. Testing with Example Automata:
   The application comes with pre-built automata for testing:
   - Load "EndsWith01.json" - Accepts binary strings ending with "01"
   - Load "EvenZeros.json" - Accepts binary strings with an even number of zeros

   To load these:
   a. Click "Load Automaton from File" in the sidebar
   b. Select the desired automaton from the list
   c. Click "Load Selected Automaton"

3. After testing the examples, you can:
   - Create your own new automata
   - Perform operations like union, intersection, complement
   - Save your automata for later use

Available Features
---------------
- Create and edit finite automata
- Check if an automaton is deterministic
- Check if an automaton is complete
- Make an automaton complete
- Convert NFA to DFA
- Minimize automata
- Check automata equivalence
- Compute union of two automata
- Compute intersection of two automata
- Compute complement of an automaton
- Test word acceptance
- Generate accepted/rejected words
- Visualize automata

File Structure
-------------
- saved_automatas/: Contains all saved automaton files (.json)
- users.db: User authentication database (SQLite)
- icon.png: Application icon
- *.py files: Application source code

Notes
-----
- The application automatically creates the saved_automatas directory if it doesn't exist
- All automata are saved in JSON format

For any issues or questions, please contact the developer at "louiziyassine003@gmail.com"


