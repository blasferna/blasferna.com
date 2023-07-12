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

  const copyButton = document.getElementById("copyButton");

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

  const copyPostUrl = function () {
    const canonicalUrl = document.querySelector('link[rel="canonical"]').href;

    const tempInput = document.createElement("input");
    tempInput.value = canonicalUrl;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    
    const originalContent = this.innerHTML;
    this.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" class="w-4 h-4 mr-2 text-green-700 dark:text-green-600">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
      ${i18n.urlCopied}
    `;

    setTimeout(function() {
        document.getElementById("copyButton").innerHTML = originalContent;
    }, 3000);
  };

  openMenu.addEventListener("click", toggleMenu);
  closeMenu.addEventListener("click", toggleMenu);

  if (copyButton) {
    copyButton.addEventListener("click", copyPostUrl);
  }

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
    let path = `/${lang}/`;
    if (lang == "en"){
      path = '/';
    }
    window.location.href = path;
  }

  let selectedLanguage = null;
  const htmlLang = document.documentElement.getAttribute("lang");
  localStorage.setItem("selectedLanguage", htmlLang);
  selectedLanguage = htmlLang;

  const langElement = document.querySelector(
    `[data-lang=${selectedLanguage}]`
  );

  if (langElement) {
    languageButton.querySelector("span").textContent =
    langElement.textContent;
  }

});
