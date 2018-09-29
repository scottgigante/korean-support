## Korean Support

Support for Korean language study for Anki 2.1.

### Features

* Automatic field filling
  * Translation (from built-in dictionary; supports English)
  * Audio (fetched from Google)
* Built-in note types (basic and advanced)

### To-do

* Romanisation (if anyone wants it)
* NAVER TTS
* Microsoft Translate

### Usage

The core feature of the add-on is the automatic field filling. To take advantage of this, you need to have an Anki note type with the appropriate fields (e.g., `Korean`, `English`, `Hanja`, `Sound`). If you don't already have such a note type, the easiest way to create one is to use the built-in model:
1. Navigate to Tools → Manage Note Types (or press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>N</kbd>)
2. Click `Add`
3. Select `Add: Korean (basic)`
4. Click `OK`
5. Click `OK` again
6. Click `Close`

Then, to use the field filling features:
1. Add a new note to Anki (press <kbd>a</kbd>)
2. Select `Korean (basic)` as the note type
3. Enable Korean Support for this note type (click `한글`)
4. Enter a word (e.g., 사랑) in the `Korean` field
5. Press <kbd>Tab</kbd>
6. The remaining fields should then be populated automatically

### History

#### v0.1-beta (2018.09.29)
* Initial port from Chinese Support
