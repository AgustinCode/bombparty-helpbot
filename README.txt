Welcome to the BombParty Bot project! This bot is designed to assist players in the online word game BombParty, operating directly within the game's chat interface.

Project Overview:   
BombParty is a fast-paced word game where players compete to guess and type words based on given themes. This bot automates certain tasks to enhance gameplay and provide assistance to players.

Features:   
    Automatic Presentation: Upon joining a game room, the bot introduces itself and its capabilities to the players.
    Real-time Message Monitoring: Monitors the chat for commands and relevant messages using Selenium and MutationObserver.
    Word Assistance: Responds to specific commands from players to suggest words containing certain syllables.
    Dynamic Wordlist: Utilizes a custom wordlist to generate suggestions based on player requests.

Interactive: Engages with players through chat interactions, responding to queries and commands promptly.


How to Use the BombParty Bot:
  Setup: Ensure you have Python installed along with necessary dependencies (selenium, webdriver, re).

  Configuration: Adjust the wordlist.txt file with words suitable for your gameplay.

  Execution: Run the bot script, which will launch a Chrome browser instance and navigate to the specified BombParty room.

  Interaction: The bot will introduce itself upon entering the room and begin monitoring chat for commands (!helpbot:[syllable]).


Contributors:
Owner   -->  AgustinCode: GitHub
Author  -->  justbrowsing37: GitHub


Future Enhancements:
  Integration with more advanced AI techniques for word suggestion.
  Support for multiple rooms and simultaneous gameplay assistance.
  Enhanced error handling and logging for better reliability.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
  Special thanks to the BombParty community for inspiration and testing.
  Thanks to the creators and maintainers of Selenium for providing a robust automation framework.


Thanks for stopping by! Feel free to fork the project and use it yourself!
