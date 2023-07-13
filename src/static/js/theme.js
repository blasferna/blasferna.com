function updateTheme() {
  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
    window.document.documentElement.style.colorScheme = "dark";
  } else {
    document.documentElement.classList.remove("dark");
    window.document.documentElement.style.colorScheme = "";
  }
}

function setLightTheme() {
  localStorage.theme = "light";
  updateTheme();
}

function setDarkTheme() {
  localStorage.theme = "dark";
  updateTheme();
}

function setSystemTheme() {
  localStorage.removeItem("theme");
  updateTheme();
}

updateTheme();
