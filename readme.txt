Automata Manager Application
========================

This application allows you to create, visualize, and analyze finite automata, including performing operations like union, intersection, and complement.

Setup Instructions
----------------
1. Make sure you have Python 3.7 or higher installed on your system.

2. Install the required dependencies by opening a terminal in this folder and running:
   pip install -r requirements.txt

3. Run the application:
   python app.py

First Time Usage
--------------
1. When you first run the application, you'll be prompted to log in.
   Default credentials:
   "admin account"
   - Username: admin
   - Password: admin123
   "normal user account"
   - user1
   - 123456789

2. After logging in, you can:
   - Create new automata
   - Load existing automata from the saved_automatas folder
   - Perform various operations on automata
   - Save your automata for future use

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
- users.db: User authentication database
- icon.png: Application icon
- *.py files: Application source code

Notes
-----
- The application automatically creates the saved_automatas directory if it doesn't exist
- All automata are saved in JSON format


For any issues or questions, please contact the developer at " louiziyassine003@gmail.com "
".