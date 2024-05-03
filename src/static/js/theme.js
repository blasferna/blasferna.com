class Theme {
  static THEME_DARK = "dark";
  static THEME_LIGHT = "light";

  static loadTheme() {
    const savedTheme = localStorage.getItem("theme");
    const darkModeMediaQuery = window.matchMedia(
      "(prefers-color-scheme: dark)"
    );
    const preferredTheme = darkModeMediaQuery.matches
      ? Theme.THEME_DARK
      : Theme.THEME_LIGHT;

    if (savedTheme) {
      document.documentElement.classList.add(savedTheme);
    } else if (preferredTheme === Theme.THEME_DARK) {
      document.documentElement.classList.add(Theme.THEME_DARK);
    }
  }

  constructor() {
    this.sunIcon = document.querySelector(".sun-icon");
    this.moonIcon = document.querySelector(".moon-icon");
    this.themeSwitcher = document.getElementById("theme-switcher");
    this.darkModeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    this.initTheme();
    this.addEventListeners();
  }

  getPreferredTheme() {
    const isDarkMode = this.darkModeMediaQuery.matches;
    return isDarkMode ? Theme.THEME_DARK : Theme.THEME_LIGHT;
  }

  toggleTheme(mode) {
    document.documentElement.classList.toggle(
      "dark",
      mode === Theme.THEME_DARK
    );
    document.documentElement.style.colorScheme =
      mode === Theme.THEME_DARK ? Theme.THEME_DARK : "";
    localStorage.setItem("theme", mode);
    this.updateIcons(mode);
  }

  updateIcons(mode) {
    if (this.sunIcon && this.moonIcon) {
      this.sunIcon.classList.toggle("hidden", mode !== Theme.THEME_DARK);
      this.moonIcon.classList.toggle("hidden", mode === Theme.THEME_DARK);
    }
  }

  initTheme() {
    const savedTheme = localStorage.getItem("theme");
    const preferredTheme = this.getPreferredTheme();
    const currentTheme = savedTheme || preferredTheme;

    this.toggleTheme(currentTheme);
  }

  handleThemeSwitch = () => {
    const currentTheme =
      localStorage.getItem("theme") || this.getPreferredTheme();
    const newTheme =
      currentTheme === Theme.THEME_DARK ? Theme.THEME_LIGHT : Theme.THEME_DARK;

    this.toggleTheme(newTheme);
  };

  handleSystemThemeChange = (e) => {
    const isDarkMode = e.matches;
    const newTheme = isDarkMode ? Theme.THEME_DARK : Theme.THEME_LIGHT;

    this.toggleTheme(newTheme);
  };

  addEventListeners() {
    this.themeSwitcher.addEventListener("click", this.handleThemeSwitch);
    this.darkModeMediaQuery.addEventListener(
      "change",
      this.handleSystemThemeChange
    );
  }
}

// The loadTheme method is static and called before the DOM is loaded. 
// This avoids the flash of the default theme before the preferred theme is applied.
Theme.loadTheme();

document.addEventListener("DOMContentLoaded", () => {
  new Theme();
});
