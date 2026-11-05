// URL de tu servidor local Django
const API_URL = 'http://127.0.0';

// Simulación de Cliente ID 1 (creado por nuestro script de poblamiento)
const CLIENTE_ID = 1;

// ID del producto que el usuario corporativo suele repetir siempre (ej: Big Mac = 1)
const PRODUCTO_FAVORITO_ID = 1; 

document.addEventListener('DOMContentLoaded', () => {
    inicializarFavorito();
    cargarMenuSimulado();
});

// Lógica de LocalStorage para Menús Favoritos
function inicializarFavorito() {
    const contenedor = document.getElementById('seccion-favorito');
    
    // Si no existe el favorito en LocalStorage, lo inicializamos por defecto para la prueba
    if (!localStorage.getItem('mcd_favorito_id')) {
        localStorage.setItem('mcd_favorito_id', PRODUCTO_FAVORITO_ID);
    }
    
    const favId = localStorage.getItem('mcd_favorito_id');
    
    // Renderizado del botón Express de Un Solo Toque
    contenedor.innerHTML = `
        <button onclick="comprarFavorito(${favId})" class="w-full bg-yellow-400 hover:bg-yellow-500 text-red-700 font-extrabold py-4 px-4 rounded-xl shadow-md flex justify-between items-center transition-transform active:scale-95 cursor-pointer">
            <span class="flex items-center gap-2">⚡ PEDIR MI BIG MAC HABITUAL</span>
            <span class="bg-red-600 text-white text-xs px-2 py-1 rounded-full">1 Clic</span>
        </button>
        <p class="text-[10px] text-gray-500 mt-2">La orden se transmite directo a la línea de cocina</p>
    `;
}

// Carga visual del menú estático coordinado con los IDs de la base de datos
function cargarMenuSimulado() {
    const lista = document.getElementById('lista-productos');
    const productosValidos = [
        { id: 1, nombre: "Big Mac", precio: "$4.990" },
        { id: 2, nombre: "Cuarto de Libra con Queso", precio: "$5.290" },
        { id: 3, nombre: "McNuggets 10 pzs", "precio": "$3.990" },
        { id: 4, nombre: "Papas Fritas Medianas", precio: "$1.890" },
        { id: 5, nombre: "Bebida Mediana", precio: "$1.500" }
    ];

    lista.innerHTML = productosValidos.map(p => `
        <div class="bg-white p-3 rounded-xl flex justify-between items-center shadow-xs border border-gray-100">
            <div>
                <h3 class="font-bold text-gray-800 text-sm">${p.nombre}</h3>
                <p class="text-red-600 font-medium text-xs">${p.precio}</p>
            </div>
            <button onclick="comprarDirecto(${p.id})" class="bg-gray-100 hover:bg-red-50 text-red-600 text-xs font-bold py-2 px-3 rounded-lg border border-gray-200 hover:border-red-200 transition-colors cursor-pointer">
                Pedir Express
            </button>
        </div>
    `).join('');
}

// Función encargada de disparar el JSON a la API REST de Django
async function enviarPedidoAPI(itemsPayload) {
    mostrarAlerta('Procesando orden express...', 'bg-blue-500');
    
    const startTime = performance.now(); // Inicio del cronómetro para verificar latencia

    try {
        const respuesta = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                idCliente: CLIENTE_ID,
                items: itemsPayload
            })
        });

        const resultado = await respuesta.json();
        const endTime = performance.now();
        const latencia = ((endTime - startTime) / 1000).toFixed(3); // Tiempo exacto de procesamiento

        if (respuesta.ok) {
            mostrarAlerta(`🎉 ¡ÉXITO! Ticket #${resultado.idPedido} enviado a cocina en ${latencia}s.`, 'bg-green-600');
        } else {
            mostrarAlerta(`❌ Error: ${resultado.error || 'Falla en transacción'}`, 'bg-red-600');
        }

    } catch (error) {
        console.error(error);
        mostrarAlerta('❌ Error de red: El servidor Django local está apagado', 'bg-red-700');
    }
}

// Handler para el botón de Orden Habitual (1 clic)
function comprarFavorito(idProducto) {
    const payload = [{ idProducto: idProducto, cantidad: 1 }];
    enviarPedidoAPI(payload);
}

// Handler para los botones individuales del catálogo
function comprarDirecto(idProducto) {
    const payload = [{ idProducto: idProducto, cantidad: 1 }];
    enviarPedidoAPI(payload);
}

// Helper para interactuar con la interfaz del smartphone
function mostrarAlerta(mensaje, claseColor) {
    const box = document.getElementById('alerta-status');
    box.className = `fixed bottom-4 left-1/2 -translate-x-1/2 w-11/12 max-w-xs text-center p-3 rounded-lg text-white font-medium shadow-lg transition-all duration-300 ${claseColor}`;
    box.innerText = mensaje;
    box.classList.remove('hidden');
}
