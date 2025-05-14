document.addEventListener('DOMContentLoaded', function() {
    
    if (typeof django_messages !== 'undefined' && django_messages && django_messages.length > 0) {
        
        django_messages.forEach(function(message) {
            const messageType = message.tags;
            
            Swal.fire({
                title: messageType === 'success' ? 'Operación Exitosa' :
                       messageType === 'error' ? 'Error' :
                       messageType === 'warning' ? 'Advertencia' : 'Información',
                text: message.text,
                type: messageType, //Si no aparece el icono, cambiar type por icon
                confirmButtonText: "OK"
            });
        });
    } else {
        console.log("No hay mensajes para mostrar o django_messages no está definido");
    }
});