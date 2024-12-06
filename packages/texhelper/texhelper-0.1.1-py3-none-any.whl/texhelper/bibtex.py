import re

def _capitalize_title(title):
    """
    Capitalize the words in the title field, except for certain small words (e.g., 'and', 'the', etc.).
    This function handles capitalization for titles in a BibTeX entry and applies special rules 
    such as capitalizing the first letter after a colon.

    Parameters:
        title (str): The title of the paper that needs to be capitalized.

    Returns:
        str: The title with proper capitalization according to title case rules.
    """
    exclude = {'and', 'or', 'nor', 'but', 'a', 'an', 'the', 'as', 'at', 'by', 'for', 'in', 'of', 'on', 'per', 'to', 'via'}
    words = title.split()
    
    capitalized_words = []
    after_colon = False  # Flag to track if we are after a colon
    
    for i, word in enumerate(words):
        # Check if the word contains a colon (':') and process accordingly
        if ':' in word:
            parts = word.split(':')
            # Capitalize the part after the colon (force first letter upper)
            parts[1] = parts[1].capitalize()  # First letter after colon should be capitalized
            capitalized_words.append(parts[0] + ':' + parts[1])  # Combine the parts back
            after_colon = True
        else:
            # Standard word capitalization, except for 'exclude' words
            if after_colon:
                capitalized_words.append(word.capitalize())
                after_colon = False
            elif word.lower() not in exclude or i == 0 or i == len(words) - 1:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word.lower())
    
    return ' '.join(capitalized_words)


def _validate_parameters(delimiter, keep_format):
    """
    Validates the parameters for the functions that process multiple titles or BibTeX entries.
    
    Parameters:
        delimiter (str): The delimiter used to join titles or entries. It should be a space (' ') if `keep_format` is True.
        keep_format (bool): Whether to preserve the format or not. If True, the delimiter must be a space.

    Raises:
        ValueError: If `keep_format` is True and the delimiter is not a space.
    """
    if keep_format and delimiter != ' ':
        raise ValueError("When keep_format is True, delimiter should not be used.")


def title_case_only(titles, delimiter=' ', keep_format=True):
    """
    Capitalize multiple titles in the given input text and format the output according to the specified options.

    Parameters:
        titles (str): A string containing one or more titles enclosed in curly braces (e.g., "{Title 1} {Title 2}").
        delimiter (str, optional): The delimiter used to join the capitalized titles. Default is a space (' ').
        keep_format (bool, optional): Whether to preserve the original curly brace format. Default is True.

    Returns:
        str: A string containing the capitalized titles, either in the original format (if `keep_format` is True)
             or joined by the specified delimiter.
    
    Raises:
        ValueError: If `keep_format` is True and the delimiter is not a space.
    """
    # Validate parameters
    _validate_parameters(delimiter, keep_format)
    
    # Split input titles by the custom delimiter
    raw_titles = re.findall(r'\{([^}]+)\}', titles)  # Match text within {}
    
    # Capitalize each title using the internal _capitalize_title function
    capitalized_titles = [_capitalize_title(title) for title in raw_titles]
    
    # Combine titles with the chosen delimiter
    if keep_format:
        return ''.join([f"{{{title}}}" for title in capitalized_titles])
    else:
        return delimiter.join(capitalized_titles)


def title_case_bibtex(bib_content, delimiter=' ', keep_format=True):
    """
    Capitalizes the title field of each BibTeX entry in the given content, preserving the rest of the fields.

    Parameters:
        bib_content (list of str): A list of strings representing the lines of a BibTeX file.
        delimiter (str, optional): The delimiter used to join the titles if not keeping format. Default is a space (' ').
        keep_format (bool, optional): Whether to preserve the original format (curly braces). Default is True.

    Returns:
        list of str: A list of strings with the capitalized titles and other fields in the same order.
    
    Raises:
        ValueError: If `keep_format` is True and the delimiter is not a space.
    """
    # Validate parameters
    _validate_parameters(delimiter, keep_format)
    
    processed_bib = []

    for line in bib_content:
        if line.strip().startswith("title={") and line.strip().endswith("},"):
            title_content = re.search(r"title={(.*)}", line).group(1)
            capitalized_title = _capitalize_title(title_content)
            
            if keep_format:
                processed_bib.append(f"title={{{capitalized_title}}},\n")
            else:
                processed_bib.append(f"{capitalized_title}{delimiter}")
        else:
            processed_bib.append(line)

    return processed_bib


def title_case_file(input_filepath, output_filepath):
    """
    Processes a .bib file, capitalizes the title field of each entry, and saves the result to a new file.
    
    Parameters:
        input_filepath (str): Path to the input .bib file.
        output_filepath (str): Path to the output .bib file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        IOError: If there are issues with reading or writing files.
    """
    # Read the input file content
    try:
        with open(input_filepath, 'r', encoding='utf-8') as file:
            bib_content = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {input_filepath} was not found.")
    
    # Process each entry in the .bib file and capitalize the title field
    processed_bib = []
    for line in bib_content:
        if line.strip().startswith("title={") and line.strip().endswith("},"):
            # Extract and capitalize the title field
            title_content = re.search(r"title={(.*)}", line).group(1)
            capitalized_title = _capitalize_title(title_content)
            processed_bib.append(f"title={{ {capitalized_title} }},\n")
        else:
            # Keep other fields unchanged
            processed_bib.append(line)
    
    # Write the processed content to the output file
    try:
        with open(output_filepath, 'w', encoding='utf-8') as file:
            file.writelines(processed_bib)
        print(f"Processed BibTeX file saved as: {output_filepath}")
    except IOError:
        raise IOError(f"Error writing to the file {output_filepath}.")


def _format_bib_entry(bib_entry):
    """
    Formats a single BibTeX entry by ensuring proper field order and stripping excess spaces.

    Parameters:
        bib_entry (str): A single BibTeX entry to be formatted.

    Returns:
        str: The formatted BibTeX entry with fields in the correct order and stripped of excess spaces.
    """
    formatted_entry = ""
    
    # Split the entry into lines (each line corresponds to a field)
    lines = bib_entry.strip().splitlines()
    
    # Strip each line and remove excess spaces
    stripped_lines = [line.strip() for line in lines]
    
    # Define the order of fields to ensure proper formatting
    field_order = ['author', 'title', 'journal', 'booktitle', 'year', 'volume', 'number', 'pages', 'publisher']
    
    # Create a dictionary to store the fields in proper order
    fields_dict = {}
    
    # Parse the lines into the dictionary
    for line in stripped_lines:
        for field in field_order:
            if line.lower().startswith(f'{field}={{'):
                fields_dict[field] = line.strip()
    
    # Reassemble the BibTeX entry with fields in the correct order
    for field in field_order:
        if field in fields_dict:
            formatted_entry += fields_dict[field] + "\n"
    
    # Return the formatted entry, removing the trailing newline
    return formatted_entry.strip()


def beautify_bibtex_file(input_file, output_file):
    """
    Format and beautify the BibTeX entries in a .bib file.

    Parameters:
        input_file (str): Path to the input .bib file.
        output_file (str): Path to the output .bib file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        IOError: If there are issues with reading or writing files.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            bib_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {input_file} was not found.")
    
    # Split the content into individual entries
    bib_entries = re.findall(r'@[\w]+\{[^@]*\}', bib_content, re.DOTALL)
    
    # Format each BibTeX entry using the private formatting function
    formatted_entries = [_format_bib_entry(entry) for entry in bib_entries]
    
    # Join the formatted entries into a single string with an empty line between them
    beautified_bib = "\n\n".join(formatted_entries)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(beautified_bib)
        print(f"Beautified BibTeX file saved as: {output_file}")
    except IOError:
        raise IOError(f"Error writing to the file {output_file}.")
