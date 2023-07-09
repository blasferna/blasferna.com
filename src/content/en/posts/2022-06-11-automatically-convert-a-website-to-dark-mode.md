---
title: Automatically convert a website to dark mode
slug: automatically-convert-a-website-to-dark-mode
date: 2022-06-11
summary: A few days ago I had the need to apply the dark mode to a website and I didn't want to spend a lot of time in the conversion process, so I started looking for a utility to facilitate the process, luckily I found Darkreader.
language: en
topic: javascript
---

![Screenshot](https://user-images.githubusercontent.com/8385910/173192842-488c18b5-16e9-42bd-8af8-f296502385dc.png)

A few days ago I had the need to apply the dark mode to a website and I didn't want to spend a lot of time in the conversion process, so I started looking for a utility to facilitate the process, luckily I found [Darkreader](https://github.com/darkreader/darkreader) an open source browser plugin that automatically applies dark mode.

Inquiring into the functionalities it offers, I found that it can be applied to a website using it as a javascript library, directly from a CDN or installed from NPM.


Today I bring a guide on how to apply it using its CDN version.

## Dependencies

* [Darkreader](https://github.com/darkreader/darkreader)

## Converting to dark mode

Add the dependency in the head of the HTML

```html
<script src="https://cdn.jsdelivr.net/npm/darkreader@4.9.46/darkreader.min.js"></script>
```

Create the toggle button to apply dark mode

```html
<input type="checkbox" id="dark-switch">
```

For the mode change to be persistent, it is necessary to store the user's preference in the browser's Local Storage.

Get user preference from Local Storage.

```javascript
  const getCurrentMode = function () {
    let mode = localStorage.getItem("mode");
    if (!mode) {
      mode = "light";
    }
    return mode;
  };
```

Function to change the mode according to the preference stored in the browser.

```javascript
  const changeMode = function (toggler) {
    let mode = getCurrentMode();
    if (toggler) {
      toggler.checked = mode === "dark";
    }
    if (mode === "dark") {
      DarkReader.setFetchMethod(window.fetch);
      DarkReader.enable({
        brightness: 100,
        contrast: 90,
        sepia: 10,
      });
    } else {
      DarkReader.disable();
    }
  };
```


The following function allows the toggler to be configured to apply the user's preference based on change events.

```javascript
 const configure = function () {
    const darkSwitch = document.getElementById("dark-switch");
    if (darkSwitch) {
      darkSwitch.addEventListener("change", function (e) {
        if (darkSwitch.checked) {
          localStorage.setItem("mode", "dark");
        } else {
          localStorage.setItem("mode", "light");
        }
        changeMode(darkSwitch);
      });
    }
    changeMode(darkSwitch);
  };
```

The following block of code allows the change to be applied safely without the user feeling the screen flicker when the library is making the change.


```javascript
  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  ready(function () {
    configure();
  });

  changeMode();
```


Create a `dark_mode.js` file to include all the code explained above:

```javascript
(function () {
  const getCurrentMode = function () {
    let mode = localStorage.getItem("mode");
    if (!mode) {
      mode = "light";
    }
    return mode;
  };

  const changeMode = function (toggler) {
    let mode = getCurrentMode();
    if (toggler) {
      toggler.checked = mode === "dark";
    }
    if (mode === "dark") {
      DarkReader.setFetchMethod(window.fetch);
      DarkReader.enable({
        brightness: 100,
        contrast: 90,
        sepia: 10,
      });
    } else {
      DarkReader.disable();
    }
  };

  const configure = function () {
    const darkSwitch = document.getElementById("dark-switch");
    if (darkSwitch) {
      darkSwitch.addEventListener("change", function (e) {
        if (darkSwitch.checked) {
          localStorage.setItem("mode", "dark");
        } else {
          localStorage.setItem("mode", "light");
        }
        changeMode(darkSwitch);
      });
    }
    changeMode(darkSwitch);
  };

  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  ready(function () {
    configure();
  });

  changeMode();
})();
```

Finally add the `dark_mode.js` in the HTML head block.

```javascript
<script type="text/javascript"  src="./dark_mode.js"></script>
```


## Demo

You can see the code in action by accessing the following link [https://blasferna.github.io/auto-dark-mode/](https://blasferna.github.io/auto-dark-mode/)

### Source

The demo page source code is available on [Github](https://github.com/blasferna/auto-dark-mode) with more details on how to apply it to a web site.

