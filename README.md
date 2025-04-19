## Korean Support

Support for Korean language study for Anki 2.1.

### Features

* Automatic field filling
  * Translation (from built-in dictionary; supports English)
  * Audio (fetched from Google)
* Built-in note types (basic and advanced)

![Edit window](https://raw.githubusercontent.com/scottgigante/korean-support/master/edit_window_demo.png)

### Instructions

* [Setup Instructions](https://github.com/scottgigante/korean-support/wiki/Setup-Instructions)
* [Frequently asked questions](https://github.com/scottgigante/korean-support/wiki/Frequently-asked-questions)
* [Learning tips](https://github.com/scottgigante/korean-support/wiki/Learning-Tips)

Use the supplied Korean (basic) or Korean (advanced) note type, or use your existing note type (just make sure your field names are called "Korean", "English", "Hanja", and "Sound".)

For bug reports, issues and feature requests, and to discuss contributing to the add-on:
* [Issue Tracker](https://github.com/scottgigante/korean-support/issues)
* [Forum support thread](https://anki.tenderapp.com/discussions/add-ons/22781-korean-support-add-on)
* [Forum development thread](https://anki.tenderapp.com/discussions/add-ons/22783-korean-support-add-on-development)
  

### Migration

With newer Anki Versions the way comments are handled changed. The plugin tries to update these templates automatically, but might detect false positives. In this case manual migration is recommended. 

Click **Browse**, select a card with the correct template, select **Cards**, go to the **Back Template** and replace `<!-- {{Sound}}-->` with `<div class=korean-support-sound>{{Sound}}</div>`, then click on **Styling** and add `.korean-support-sound { display: none; }` to the bottom as a new line.

### To-do

* Romanisation (if anyone wants it)
* NAVER Translate
* Microsoft Translate
* Google Translate

### History

### v0.20-beta
* Migrate sound templates to work with newer Anki

### v0.19-beta (2024.05.25)
* Remove deprecated anki calls and fix version in about section

#### v0.18-beta (2024.02.24)
* Bugfix to menu load on profile switch.

#### v0.17-beta (2024.02.13)
* Bugfix to PyQT compatibility

#### v0.14-beta (2024.02.02)
* Anki 23.10 compatibility update
* Update to PyQT6

#### v0.13-beta (2021.07.31)
* Update Google TTS submodule

#### v0.12-beta (2021.05.21)
* Bugfix

#### v0.11-beta (2021.02.24)
* Add 'fill missing hanja' function

#### v0.10-beta (2021.02.04)
* Update Google TTS submodule

#### v0.9-beta (2021.01.21)
* Updated to new version of NaverTTS using CLOVA dictionary API and fix Google TTS.

#### v0.8-beta (2020.04.14)
* Added gender and speed selection for TTS

#### v0.7-beta (2020.04.05)
* Bugfix

#### v0.6-beta (2020.01.30)
* Anki 2.1.20 compatibility update

#### v0.5-beta (2020.01.02)
* Added NAVER TTS

#### v0.4-beta (2019.12.30)
* Made automatic updates more conservative

#### v0.3-beta (2018.12.31)
* Added debug mode

#### v0.2-beta (2018.11.30)
* Update Google TTS submodule

#### v0.1-beta (2018.09.29)
* Initial port from Chinese Support
