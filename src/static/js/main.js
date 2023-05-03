/**
 * $(document).ready() in pure javascript.
 * @param {*} fn
 */
function ready(fn) {
  if (document.readyState !== "loading") {
    fn();
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
}

ready(function () {
  const openMenu = document.getElementById("openMenu");
  const closeMenu = document.getElementById("closeMenu");
  const hiddenMenu = document.getElementById("hiddenMenu");

  const languageButton = document.getElementById("languageButton");
  const languageList = document.getElementById("languageList");
  const languageItems = document.querySelectorAll('[role="menuitem"]');

  const toggleMenu = function () {
    let isOpen = hiddenMenu.classList.contains("translate-x-0");

    if (isOpen) {
      hiddenMenu.classList.add("translate-x-full");
      hiddenMenu.classList.remove("translate-x-0");
    } else {
      hiddenMenu.classList.add("translate-x-0");
      hiddenMenu.classList.remove("translate-x-full");
    }
  };

  openMenu.addEventListener("click", toggleMenu);
  closeMenu.addEventListener("click", toggleMenu);

  languageButton.addEventListener("click", () => {
    languageList.classList.toggle("hidden");
  });

  languageItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const lang = item.getAttribute("data-lang");
      handleLanguageSelection(lang);
      languageList.classList.add("hidden");
      languageButton.querySelector("span").textContent = item.textContent;
    });
  });

  function handleLanguageSelection(lang) {
    localStorage.setItem("selectedLanguage", lang);
    window.location.href = `/${lang}/`
  }

  const storedLanguage = localStorage.getItem("selectedLanguage");
  var selectedLanguage = null;

  if (storedLanguage) {
    selectedLanguage = storedLanguage;
  } else {
    const htmlLang = document.documentElement.getAttribute("lang");
    localStorage.setItem("selectedLanguage", htmlLang);
    selectedLanguage = htmlLang;
  }

  const storedLanguageItem = document.querySelector(
    `[data-lang=${selectedLanguage}]`
  );

  if (storedLanguageItem) {
    languageButton.querySelector("span").textContent =
      storedLanguageItem.textContent;
  }
});
