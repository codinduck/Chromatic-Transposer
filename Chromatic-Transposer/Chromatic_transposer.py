import tkinter as tk
from tkinter import messagebox
import re

# chromatic scale
CHROMATIC_SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# Function to find the index of a chord in the chromatic scale
def find_chord_index(chord):
    for i, note in enumerate(CHROMATIC_SCALE):
        if chord.startswith(note):
            return i, note
    return None, None


def transpose_chord(chord, semitone_diff):
    index, root_note = find_chord_index(chord)
    if index is None:
        return chord  # Return the chord as is if it's not a recognized chord

    # Transpose the root note
    new_index = (index + semitone_diff) % len(CHROMATIC_SCALE)
    new_chord = CHROMATIC_SCALE[new_index]

    # Add any suffix (e.g., minor "m", 7th "7") back to the chord
    return new_chord + chord[len(root_note):]


def transpose_line_preserving_spacing(line, semitone_diff):
    transposed_line = ""
    i = 0
    while i < len(line):
        match = re.match(r"[A-G](#|b)?(m|M|dim|aug|sus|add|maj|[0-9])*", line[i:])
        if match:
            chord = match.group(0)
            transposed_chord = transpose_chord(chord, semitone_diff)
            transposed_line += transposed_chord
            i += len(chord)
        else:
            transposed_line += line[i]
            i += 1
    return transposed_line


# Main function to transpose chords in lyrics
def transpose_lyrics(original_key, target_key, lyrics_with_chords):
    try:
        semitone_diff = (CHROMATIC_SCALE.index(target_key) - CHROMATIC_SCALE.index(original_key)) % len(CHROMATIC_SCALE)
    except ValueError:
        messagebox.showerror("Error", "Invalid key entered. Please check the keys and try again.")
        return ""

    # Process lyrics line by line
    lines = lyrics_with_chords.split("\n")
    transposed_lines = []

    for line in lines:
        if line.strip() == "":
            transposed_lines.append("")
        elif re.match(r"^[A-G](#|b)?", line.strip()):  # Check if the line starts with a chord
            transposed_lines.append(transpose_line_preserving_spacing(line, semitone_diff))
        else:  # Treat the line as lyrics
            transposed_lines.append(line)

    return "\n".join(transposed_lines)


# Create the GUI
def create_gui():
    def on_transpose():
        original_key = original_key_entry.get().strip()
        target_key = target_key_entry.get().strip()
        lyrics_with_chords = lyrics_text.get("1.0", tk.END).strip()

        if not original_key or not target_key or not lyrics_with_chords:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        transposed = transpose_lyrics(original_key, target_key, lyrics_with_chords)
        if transposed:
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", transposed)

    # main window
    window = tk.Tk()
    window.title("Chord Transposer")
    window.geometry("600x600")

    # Input for original key
    tk.Label(window, text="Original Key:").pack(pady=5)
    original_key_entry = tk.Entry(window)
    original_key_entry.pack(pady=5)

    # Input for target key
    tk.Label(window, text="Target Key:").pack(pady=5)
    target_key_entry = tk.Entry(window)
    target_key_entry.pack(pady=5)

    # Input for lyrics and chords
    tk.Label(window, text="Lyrics with Chords:").pack(pady=5)
    lyrics_text = tk.Text(window, height=10, wrap=tk.WORD)
    lyrics_text.pack(pady=5)

    # Transpose button
    transpose_button = tk.Button(window, text="Transpose", command=on_transpose)
    transpose_button.pack(pady=10)

    # Output area for transposed lyrics
    tk.Label(window, text="Transposed Lyrics with Chords:").pack(pady=5)
    result_text = tk.Text(window, height=10, wrap=tk.WORD)
    result_text.pack(pady=5)

    # Run the GUI loop
    window.mainloop()


create_gui()
