###########################################################
#  Project #6
#
#  Algorithm
#    Prompt for a text file of stop words (words to exclude)
#    Prompt for a CSV file containing the artist, song, and lyrics.
#    call functions to build a table of the top 10 artists, their average word
#      count, vocabulary size, and number of songs.
#    Ask user to search lyrics by words, input space seperated words.
#    Display table of top 6 artists and song pairs containing those words.
#    Loop to continue searching words
#    User types enter to end program.
###########################################################

import csv
import string
from operator import itemgetter

def open_file(message):
    '''This function prompts the user to enter a filename displaying the message provided. The program will try to
open a file. It should have a try-except statement. An error message should be shown if the file cannot be
opened and reprompt for the new filename. If the file is successfully opened, it returns a file object.'''
    input_message = input(message)
    try:
        open_file = open(input_message, 'r')
        return open_file
    except FileNotFoundError:
        print("File is not found! Try Again!")

def read_stopwords(fp):
    '''This function receives a file pointer (for the stopwords.txt file) as a parameter (such as returned from
open_file(message)) and returns a set of unique stop words. All of the words should be converted to
lower case. Remember to close the file inside the function after you are done reading it.'''
    stopwords = set()
    for line in fp:
        line = line.strip()
        line = line.lower()
        stopwords.add(line)
    return stopwords
        

def validate_word(word, stopwords):
    '''This function receives a string (word) and a set (stopwords) as parameters. If the given word is in the stop
word set or it has any digit or punctuation, the function returns False. Otherwise, it returns True. (For an
extra challenge, using Boolean operators can reduce this function to one line.)'''
    if word in stopwords:
        return False
    for char in word:
        if char.isdigit():
            return False
        if char in string.punctuation:
            return False
    return True

def process_lyrics(lyrics, stopwords):
    '''This function receives a string (lyrics) and a set of stop words (stopwords) as parameters. The string
contains the lyrics. The function splits the lyrics by space. Each word is made lower case and stripped of
whitespace and then punctuation. After that it validates each word by using the validate_word function. If
the word is valid, it adds that word to a set which will be returned after all words are processed.
Note: Do not forget to convert the words to lowercase and strip punctuation from the end of words (if there is
something like a hyphen in the middle of a string, we will not strip it).
Hint: string.punctuation is useful.'''
    lyrics = lyrics.split()
    lyrics_set = set()
    for word in lyrics:
        word = word.lower()
        word = word.strip(string.punctuation)
        if word == "":
            continue
        elif validate_word(word, stopwords) == True:
            lyrics_set.add(word)
    return lyrics_set

def read_data(fp, stopwords):
    '''This function has two parameters, the file pointer for a csv file and a set of stop words. It reads in the data
collecting 3 things from each row: singer name as a string, song name as a string and lyrics as a string. You
should iterate through the file line by line and for every line, you should read singer name, song name and the
entire lyrics of that song which consists of many lines. You should convert the lyrics to lowercase. Then by
using process_lyrics function you should process the lyrics to create a set of words. After that, you can
update the dictionary by using update_dictionary function and passing the values you read. Finally, it
should return the dictionary. Remember to close the file inside the function after you are done reading it.'''
    data_dict = {}
    csv_reader = csv.reader(fp)
    #iterate through each row. Skip the header row
    next(csv_reader)
    for row in csv_reader:
        singer = row[0]
        song = row[1]
        lyrics = row[2]
        lyrics = lyrics.lower()
        words = process_lyrics(lyrics, stopwords)
        update_dictionary(data_dict, singer, song, words)
    return data_dict

def update_dictionary(data_dict, singer, song, words):
    '''This function receives a data dictionary (data_dict), singer’s name (singer), song’s name (song_name),
and a set of words (song_words_set) as parameters. The data_dict is a dictionary of singers (the key),
and each value is a dictionary of all the signer’s songs (song_dict). The song_dict is a dictionary of
song_name: song_words_set key-value pairs. This function inserts a song_name:
song_words_set key-value pair to the song_dict dictionary of the singer. It does not return anything.
The following is how we want the data_dict to be formatted:
{"singer1":{"song1": set_of_words, "song2": set_of_words,…},
 "singer2":{…},
 "singer3":{…},
 …}'''
    if singer not in data_dict:  #  if singer is not in data_dict
        data_dict[singer] = {}  #  add singer to data_dict
    data_dict[singer][song] = words  #  add song to singer's dictionary
    pass
        
def calculate_average_word_count(data_dict):
    '''This function receives data_dict (which is created by the read_data function) and returns another
dictionary which contains average word counts of singers.
We define average word count for a singer as the total number of words used by that singer, divided by the
number of songs of the singer.
You should do this calculation for every singer and store the results in a dictionary and return it.
Here is the format of the dictionary:
dict{"singer1": average, "singer2": average,…}'''
    average_dict = {}
    for singer in data_dict:
        total_words = 0
        for song in data_dict[singer]:  #  For every song in singer's dictionary
            total_words += len(data_dict[singer][song])  #  add the length of the song to total_words
        average = total_words / len(data_dict[singer])  #  divide total words by number of songs to find average
        average_dict[singer] = average
    return average_dict

def find_singers_vocab(data_dict):
    '''This function receives data_dict (which is created by read_data function) and returns another dictionary
which contains set of distinct words used by every singer. To create a set of vocabulary for a singer, you should
find the union of all the words that are used by that singer. Finally, the function returns a dictionary in this
format:
dict{"singer1": set1, "singer2": set2,…}'''
    vocab_dict = {}
    for singer in data_dict:
        vocab_set = set()
        for song in data_dict[singer]:
            vocab_set = vocab_set.union(data_dict[singer][song])
        vocab_dict[singer] = vocab_set
    return vocab_dict

def display_singers(combined_list):
    '''This function receives a list which is created in the main function and it includes a tuple for every singer. Each
tuple should have the following data:
(singer name, average word count, number of songs, vocabulary size)
where vocabulary size is the number of distinct words used in the singer’s songs.
This function sorts the list by average word count in descending order. If two tuples have the same average, it
sorts them by the vocabulary size, again in descending order. If two tuples have the same average and same
vocabulary size, keep the same order as it appears in the combined_list list.
Hint: itemgetter is useful for sorting by multiple items. What happen when you specify an item to sort
with using itemgetter and there is a tie?
Finally, it prints the top ten tuples after sorting the list in the given format.'''
    #if two tuples don't have the same average, sort them by average word count in descending order
    combined_list.sort(key=itemgetter(1), reverse=True)
    #if two tuples have the same average, sort them by vocabulary size in descending order
    if combined_list[0][1] == combined_list[1][1]:
        combined_list.sort(key=itemgetter(2), reverse=True)
    #  print the top ten tuples after sorting the list in the given format
    print("\n{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer","Average Word Count", "Vocabulary Size", "Number of Songs"))
    print('-' * 80)
    for i in range(10):
        print("{:<20s}{:>20.2f}{:>20d}{:>20d}".format(combined_list[i][0], combined_list[i][1], combined_list[i][2], combined_list[i][3]))
    pass


def search_songs(data_dict, words):
    '''This function receives data_dict and a set of words which includes the words of the given query. It creates a list
of tuples (singer name, song name) every time it finds a match. If a song includes every word in the given word
set, you should include that song and the singer of that song in the output list. Before you return the list, you
should sort it by singer name in alphabetical order and if two tuples have the same singer, you should sort them
by song name (again, alphabetical order).
Hint: subset is useful'''
    song_list = []
    for singer in data_dict:
        for song in data_dict[singer]:
            if words.issubset(data_dict[singer][song]):
                song_list.append((singer, song))
    #  Sort first by singer name in alphabetical order, then by song name
    song_list.sort(key=itemgetter(0, 1))
    return song_list


def main():
    '''In the main function, stop words and song data will be read by using the appropriate function calls.
After that, the average word count and vocabulary will be calculated for every singer. To be able to display the
results, the output of these functions should be combined in the following format: (singer name, number of
songs, average word count, vocabulary size). Since there will be a tuple for every singer, you should create a list
to store these tuples. The list could be used to display the results. Then, you need to prompt to get a set of words
to search through lyrics. The words are separated by space. After searching, you should print the top 5 results.
Your program shouldn’t crash if it returns fewer results. You can check the test cases for more information.'''

    #prompt user to enter a filename for the stopwords
    stopwords = open_file("\nEnter a filename for the stopwords: ")
    #read stopwords
    stopwords = read_stopwords(stopwords)
    #prompt user to enter a filename for the song data
    song_data = open_file("\nEnter a filename for the song data: ")
    #read song data
    song_data = read_data(song_data, stopwords)
    #calculate average word count
    average_dict = calculate_average_word_count(song_data)
    #calculate vocabulary
    vocab_dict = find_singers_vocab(song_data)
    #combine the results
    combined_list = []
    for singer in song_data:
        combined_list.append((singer, (average_dict[singer]), len(vocab_dict[singer]), len(song_data[singer])))
    #display the results
    display_singers(combined_list)
    #prompt user to enter a set of words
    words = input("\nSearch Lyrics by Words\n\nInput a set of words (space separated), press enter to exit: ")
    while words != "":
    #  if stopword was entered or punctuation, prompt user to enter a set of words again
        for word in words.split():
            if not validate_word(word.lower(), stopwords):
                print("\nError in words!\n1-) Words should not have any digit or punctuation\n2-) Word list should not include any stop-word")
                words = input("\nInput a set of words (space separated), press enter to exit: ")
                continue
        words = words.lower()
        words = words.split()
        words = set(words)
        #search songs
        song_list = search_songs(song_data, words)
        #print the results
        print("\nThere are {} songs containing the given words!".format(len(song_list)))
        #  if there are 0 results for the given words, prompt user to enter a set of words again
        if len(song_list) == 0:
            words = input("\nInput a set of words (space separated), press enter to exit: ")
            continue
        print("{:<20s} {:<s}".format("Singer", "Song"))
        if len(song_list) >= 5:
            for i in range(5):
                print("{:<20s} {:<s}".format(song_list[i][0], song_list[i][1]))
        #  if there are less than 5 results for the given words, print all the results
        if len(song_list) < 5:
            for i in range(len(song_list)):
                print("{:<20s} {:<s}".format(song_list[i][0], song_list[i][1]))
        #prompt user to enter a set of words
        words = input("\nInput a set of words (space separated), press enter to exit: ")
    pass

if __name__ == '__main__':
    main()           
