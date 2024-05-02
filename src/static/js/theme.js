function updateTheme() {
  const isDarkMode =
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches);

  document.documentElement.classList.toggle("dark", isDarkMode);
  window.document.documentElement.style.colorScheme = isDarkMode ? "dark" : "";
}

function setLightTheme() {
  localStorage.setItem("theme", "light");
  updateTheme();
}

function setDarkTheme() {
  localStorage.setItem("theme", "dark");
  updateTheme();
}

function setSystemTheme() {
  localStorage.removeItem("theme");
  updateTheme();
}

updateTheme();
