---
title: Evita Peticiones Excesivas con Debounce
slug: evita-peticiones-excesivas-con-debounce
date: 2024-11-12
summary: Aprende a implementar la técnica de debounce para optimizar las peticiones al servidor y mejorar el rendimiento de tu aplicación.
language: es
tags:
  - javascript
  - performance
  - frontend
---

Cuando desarrollamos aplicaciones web, es común necesitar realizar peticiones al backend mientras el usuario ingresa datos en campos de texto, como por ejemplo en un buscador. Si bien esto no representa un problema en aplicaciones con poco tráfico, la situación cambia drásticamente en sistemas que manejan miles de usuarios simultáneos. En estos casos, cada pulsación de tecla podría generar una petición que interactúe con la base de datos, lo que puede ocasionar serios problemas de rendimiento.

Para solucionar esto, necesitamos implementar un mecanismo que controle la frecuencia de las peticiones. En lugar de crear un algoritmo desde cero, podemos utilizar una técnica probada y eficiente conocida como **debounce** (función de rebote), que nos permite gestionar estas solicitudes de manera óptima.

El debounce funciona como un temporizador inteligente que espera a que el usuario termine de escribir antes de ejecutar la acción. Por ejemplo, si establecemos un tiempo de espera de 500 milisegundos, la función debounce:

1. Detecta la primera pulsación de tecla pero no ejecuta la petición inmediatamente
2. Inicia un temporizador de 500ms
3. Si el usuario presiona otra tecla antes de que termine el tiempo, reinicia el temporizador
4. Solo cuando el usuario deja de escribir y pasan los 500ms, se ejecuta finalmente la petición

Esto significa que si un usuario escribe "programación" rápidamente, en lugar de realizar 12 peticiones (una por cada letra), solo se ejecutará una única petición con la palabra completa.

Veamos un ejemplo práctico de implementación:

```javascript
function debounce(func, wait) {
  let timeout;

  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Ejemplo de uso
const searchProducts = debounce((text) => {
  // Realizar petición al backend
  console.log('Searching:', text);
}, 500);

// En el campo de búsqueda
searchInput.addEventListener('input', (e) => {
  searchProducts(e.target.value);
});

```

Con esta técnica, logramos una mejor experiencia para el usuario y reducimos la carga en nuestros servidores al minimizar las peticiones innecesarias.

