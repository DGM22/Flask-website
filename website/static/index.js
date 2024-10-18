function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    }); 
};


function mostrarContenidoSegunTamanio() {
    const mobileContent = document.querySelector('#estilo_mobil');
    const desktopContent = document.querySelector('#estilo_laptop');

    // Detectar el tamaño de la pantalla
    if (window.innerWidth <= 767) {
        // Mostrar contenido móvil
        mobileContent.style.display = 'block';
    } else {
        // Mostrar contenido de escritorio
        mobileContent.style.display = 'none';
    }
};

// Ejecutar la función al cargar la página
mostrarContenidoSegunTamanio();

// También puedes ejecutar la función cuando la ventana se redimensiona
window.addEventListener('resize', mostrarContenidoSegunTamanio());
