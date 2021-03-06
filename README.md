# README

### Disclaimer
This is an ever evolving project, and is subject to substantial changes and bugs at all times. 
You are welcome to use anything in this project that you find helpful, but do so at your own risk. 
I do not provide support, however if you would like to contact me I welcome productive communication.

---

## How To Use 

### JSON Data Structure

*Example of a json data entry*
```
"002656": {
        "type": "note_on",
        "frame": 5368,
        "note": 84,
        "value": 106
    }
```
 - "002656" - the index of this event, always increases by 1
 - "type" - gives information on what event this is, usually note_on, note_off, or control_change
 - "frame" - frame that the event occurs on, as defined by your settings, can increase by any amount
 - "note" - which note out of 0-127 MIDI notes is being modified
 - "value" - the intensity or extent of the action, the expected range is 0-127
 
 Notes: Data input can be changed per entry type, it is important to check entry type before processing the entry
 
 ### Blender Animator Script
 To use the script, simply open it in Blender and ensure your target objects are named appropriately. The method I use is to name them 000-127 since it is the simplest option, however it is pretty trivial to change the script to meet your needs if you understand Python. 
 
 **Things to pay attention to:**
  - Project FPS and generated data FPS, a mismatch will result in improperly synced animations
  - This script currently only animates one object per note/entry so ensure your animations are all driven by that one object
  - Put target anim objects in a separate collection to make purging anim data easier if you get it wrong
  - Consider limiting scope of the search for anim objects if your naming scheme is not unique
 
**Blender Version:**
  While I will attempt to keep from using version specific methods, I only use the script with the latest version of Blender.
 Previous versions may still work fine, however be prepared to encounter unexpected issues and self diagnose/repair.
 
 ***This is a personal project and is provided as-is with no warranty, real or implied***

---

## Features and Updates

### Midi Conversion:
 
*Convert MIDI files to a variety of more useful data types*
 - Convert MIDI files to a simple dictionary containing necessary data for animation depending on your chosen frame rate
 - Save dictionary to .JSON files for easy access with broad compatibility
 - Maintain a local SQLite3 database of all converted MIDI files
 - Export an image displaying classic MIDI bars for every note event
 - Export sliced images for an animated texture at your set frame rate 
 
 ### Blender Animation: 

*Animate a range of objects by name and index with previously defined animation data* 
  - Calculate animation smoothing based on user inputs and key velocity
  - Set rotational keyframes based on event note number and object name
  - Set object color based on note number and object name (useful in shaders)
  
  
---
