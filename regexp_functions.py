import re
import os
import shutil

def translate_to_saltylang(text: str) -> str:
    '''
    Translate Russian text into "salty language".

    After every vowel inserts the letter "с" and the same vowel.
    Example: "привет" -> "присивесет". All other characters are unchanged.

    Arguments:
    text: str - Russian text to translate

    Returns:
        str: Translated text.
    '''
    pattern = r"([аеёиоуыэюяАЕЁИОУЫЭЮЯ])"

    def repl(match):
        vowel = match.group(1)
        return f"{vowel}с{vowel.lower()}"
    return re.sub(pattern = pattern, repl = repl, string = text)


def get_chords(song_file: str) -> set:
    '''
    Returns the set of chords found in a song text file.

    Work only with Russian songs, where the lyrics are 
    written in Cyrillic and the chords in Latin letters A-G with an optional "m".

    Arguments:
    song_file: str - path to a file with song lyrics and chords

    Returns:
        set: A set of unique chords names.
    '''
    pattern = r"\b[A-G]m?\b"
    chords = []
    with open(song_file) as file:
        for line in file:
            matched_patterns = re.findall(pattern, line)
            chords += matched_patterns
    return set(chords)


def rename_files(dir, 
                 pattern, 
                 new_pattern = None, 
                 sample_names: dict = None, 
                 to_replace: bool = False) -> None:
    '''
    Performs group renaming of files selected by the regular expression `pattern`. 
    For each of selected files it builds a new name: first it replaces the part matched by `pattern` 
    with `new_pattern`, and then it renames samples using `sample_names`. 
    The new files are created in the same directory.

    Arguments:
    dir: directory with files to rename
    pattern: regular expression used to select files; the matched part 
             of the name is replaced with `new_pattern`
    new_pattern: the string that replaces the file names. If it is None, then renaming according to the pattern 
                 does not occur, but the original `pattern` is required to select files
    sample_names: a dictionary that sets the rules for renaming samples
    to_replace: rename files with deletion of the original (True) or 
                       just with copying (False). By default False.

    Returns None.
    '''

    dir_content = []
    for f in os.listdir(dir):
        if re.search(pattern, f):
            dir_content.append(f)
            
    renamed_files = []

    if new_pattern is not None:
        for filename in dir_content:
            updated_filename = re.sub(pattern, new_pattern, filename)
            renamed_files.append(updated_filename)
    else:
        renamed_files = dir_content

    final_file_names = []
    for re_filename in renamed_files:
        if sample_names is not None:
            for key, value in sample_names.items():
                re_filename = re_filename.replace(key, value)
        final_file_names.append(re_filename)

    names_dict = dict(zip(dir_content, final_file_names))

    for old_name, new_name in names_dict.items():
        if old_name == new_name:
            continue
        old_path = os.path.join(dir, old_name)
        new_path = os.path.join(dir, new_name)
        if to_replace:
            os.rename(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)   