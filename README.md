# A Sublime Text 2 plugin to show build output in a view.

In Sublime Text 2, build results are shown in a fixed horizontal panel; you
can't drag it to put it vertically next to your code, like in Eclipse, VS.

With this plugin, like any other view, you can put your build results where
you want:

![buildview vertical](https://github.com/rctay/sublime-text-2-buildview/raw/master/buildview.png)

The core functionality is done in `pipe_views.PipeViews`, an abstraction
allowing Unix-like "pipes" to be created between Views in Sublime.

# Usage

The plugin hooks on to the keyboard shortcuts for launching builds; if you
have different shortcuts for them, change the `.sublime-keymap` files
accordingly. These bindings **must** have the following context:

	"context": [{"key": "build_fake", "operator":"equal", "operand":true}]

## Output scrolling

The plugin can scroll the output to the top, bottom, or the position before
the current build was launched. (The default is to scroll to the bottom.)
This can be specified by triggering the Command Palette in *any* view (view
with build output or with source code) in the window, and selecting one of

    Build output always at top
    Build output always at end
    Build output stays at same position

The default setting can also be specified. It is read as the value to the key
`buildview_scroll` from Sublime's Settings (ie. user/default
`Preferences.sublime-settings`) and is one of

 - `top`
 - `bottom`
 - `last`

## Disabling

The plugin can be disabled on a per-view basis by triggering the Command
Palette in either the view with build output or with source code and selecting

    Disable/Enable buildview for this window

# Issues/TODO

 - build view does not gain focus if it is in the same tab group as the view
   that launched the build
 - pin/unpin location, so that subsequent builds scrolls to the same location
 - build view is "forgotten" after restarting Sublime
 - improve disabling/enabling options (eg whitelists, blacklists)

Pull requests welcome!

# Hacking notes

 - after editing `pipe_views.py`, restart Sublime or re-save `commands.py` 
   for the changes to take effect.
 - _who's view is it anyway?_ A variety of names are used for views in the
   source code, according to their different roles:
   - source view: the built-in view that shows up when you click Show Build
     Results
   - destination view: the view that mirrors the build output, the one with the
     title "Build Output"
   - otherwise, a view should generally refer to one holding the source for the
     build
