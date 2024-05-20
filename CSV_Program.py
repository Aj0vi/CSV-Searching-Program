"""
#############################################################################
#   Algorithm
#       Prompt for a stopwords.txt and songdata.csv
#       Initialize:
#           -Read the songdata and create a dictionary from it
#           -Find the average word count for each song from the songdata
#            dictionary. Create a dictionary from that
#           -Find the unique words from the songdata dictionary. Create a
#            dictionary from that
#       Loop to print the top 10 singers by average word count
#       Loop to search for songs by lyrics
#           Prompt for a valid lyric
#           Print the amount of song with the lyric
#           Print, at most, the first 5 singers
#           Prompt to continue or discontinue
##############################################################################
"""

import csv
import string
from operator import itemgetter


def open_file(message):
    """Returns a file object when a valid file name is given.
    message: A message for what file should be opened (str)
    Returns: A file object (file)
    """
    while True:
        try:
            file_name = input(message)
            fp = open(file_name)
            return fp
        except:
            print("\nFile is not found! Try Again!")


def read_stopwords(fp):
    """Reads a text file and returns a set of unique stop words.
    fp: A text file of stop words to read from (file)
    Returns: A set of unique stop words (set)
    """
    stop_set = {(word.lower()).strip() for word in fp}
    fp.close()
    return stop_set


def validate_word(word, stopwords):
    """Validates if the word is not in the stopwords set or not.
    word: The word to be validated (str)
    stopwords: The set used to validate the word parameter (set)
    Returns: True if the word is letters a-z and not in words. Otherwise,
    False (bool)
    """
    # Checks if the word is valid.
    return True if (word not in stopwords and word.isalpha()) else False


def process_lyrics(lyrics, stopwords):
    """Returns a set of the words that returned true from validate_word().
    lyrics: String that will be split to make a list of words to validate (str)
    stopwords: Set used in validate_word() to validate a word from lyrics (set)
    """
    word_list = [(word.lower()).strip().strip(string.punctuation) for word in
                 lyrics.split()]
    processed_set = set()
    for word in word_list:
        if validate_word(word, stopwords):
            processed_set.add(word)
    return processed_set


def read_data(fp, stopwords):
    """Reads a csv of song data to return a new/updated dictionary matrix.
    fp: The csv file pointer that's read (file)
    stopwords: The set of words used to use process_words() and
               update_dictionary() (set)
    Returns: An updated dictionary from the csv file of song data (dict)
    """
    data_dict = {}
    reader = csv.reader(fp)
    next(reader)
    for line in reader:
        # line[2] is the lyrics; line[0] is the singer; line[1] is the song.
        word_set = process_lyrics(line[2].lower(), stopwords)
        update_dictionary(data_dict, line[0], line[1], word_set)
    fp.close()
    return data_dict


def update_dictionary(data_dict, singer, song, words):
    """Inserts a dictionary(song:words) into data_dict for the respective
       artist.
    data_dict: A dictionary of singers where each value is a dictionary
               of songs (dict)
    singer: The key of data_dict (str)
    song: The value of data_dict. Also, the key of the nested dictionary
    inside of data_dict (str)
    word: The value of song (set)
    Returns: None
    """
    # Creates a new key if it doesn't exist, otherwise it updates the
    # existing key.
    if singer not in data_dict:
        data_dict[singer] = {song: words}
    else:
        data_dict[singer].update({song: words})


def calculate_average_word_count(data_dict):
    """Returns a dictionary of each singer's average word count in their
       songs.
    data_dict: A dictionary created by read_data() (dict)
    Returns: A dictionary of each singer's average word count in their
             songs (dict)
    """
    average_dict = {}
    for singer, songs in data_dict.items():
        song_total = len(songs.keys())
        word_total = 0
        for word_set in songs.values():
            # word_set is the lyrics set; the value of the song key.
            word_total += len(word_set)
        average = word_total / song_total
        average_dict[singer] = average
    return average_dict


def find_singers_vocab(data_dict):
    """Uses data_dict to return a dictionary of all the distinct words
       used by every singer.
    data_dict: A dictionary that'll be iterated through to create a new
               dictionary (dict)
    Returns: A dictionary of all the distinct words used by every singer (dict)
    """
    vocab_dict = dict()
    for singer, songs in data_dict.items():
        union_set = set()
        for word_set in songs.values():
            for word in word_set:
                union_set.add(word)
        # union_set creates a union with itself, removing duplicate words.
        vocab_dict[singer] = union_set.union()
    return vocab_dict


def display_singers(combined_list):
    """Prints out a list of the top 10 singers by word count from the list.
    combined_list: A list of the top 10 singers by word count in descending
                   order (list)
    Returns: None
    """

    print("\n{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer", "Average Word Count",
                                                "Vocabulary Size", "Number of "
                                                                   "Songs"))
    print('-' * 80)
    # reverse=True was used to make the list descending.
    singers_list = sorted(combined_list, key=itemgetter(1, 3), reverse=True)
    for tuple_singer in singers_list[:10]:
        singer, avg_word, song_total, vocab_size = tuple_singer
        print(f"{singer:<20}{avg_word:>20.2f}{song_total:>20}{vocab_size:>20}")


def search_songs(data_dict, words):
    """Searched for the songs that have the most in common with the lyrics
       given.
    data_dict: A dictionary matrix of the artists,songs, and their lyrics
               (dict)
    words: A set of lyrics used match with a song from data_dict (set)
    Returns: A list of the songs that matched the lyrics given by word (list)
    """
    match_list = []
    for singer, songs in data_dict.items():
        for song_name in songs:
            if words.issubset(songs[song_name]):
                match_list.append((singer, song_name))
    match_list = sorted(match_list, key=itemgetter(0, 1))
    return match_list


def validate_set(word_set, stopwords):
    """Checks if each word in a set is valid according to validate_word().
    word_set: Lyrics given by the user (set)
    stopwords: Used to check the validity of each word in word_set (set)
    Returns: True if all the words are valid. Otherwise, False (bool)
    """
    for word in word_set:
        # Checks each word in the set and returns False if it finds one
        # invalid word.
        if not validate_word(word, stopwords):
            return False
    return True


def main():
    stopwords = read_stopwords(open_file('\nEnter a filename for the '
                                         'stopwords: '))
    fp = open_file('\nEnter a filename for the song data: ')
    data_dict = read_data(fp, stopwords)
    average_words = calculate_average_word_count(data_dict)
    distinct_vocab = find_singers_vocab(data_dict)

    singers_list = []
    for singer, songs in data_dict.items():
        song_total = len(songs.keys())
        vocab_size = len(distinct_vocab[singer])
        singers_list.append((singer, average_words[singer], vocab_size,
                             song_total))
    display_singers(singers_list)

    print("\nSearch Lyrics by Words")
    while True:
        user_set = set(input("\nInput a set of words (space separated), "
                             "press enter to exit: ").lower().split())
        # Pressing enter creates an empty set in this case.
        if user_set == set():
            break
        elif not validate_set(user_set, stopwords):
            print('\nError in words!')
            print('1-) Words should not have any digit or punctuation')
            print('2-) Word list should not include any stop-word')
            continue
        else:
            searched_list = search_songs(data_dict, user_set)

            if len(searched_list) == 0:
                print(f"\nThere are {len(searched_list)} songs containing the "
                      f"given words!")
                continue
            else:
                print(f"\nThere are {len(searched_list)} songs containing the "
                      f"given words!")

                print(f"{'Singer':<20s} {'Song':<s}")
                for line in searched_list[:5]:
                    singer, song = line
                    print(f"{singer:<20s} {song:<s}")


if __name__ == '__main__':
    main()
