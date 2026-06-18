---
aside: false
outline: false
---

# Índice de Gramática

El Índice Gramatical enumera todos los temas y fenómenos gramáticos del curso de sánscrito y permite un acceso rápido a lecciones específicas.

&lt;!DOCTYPE html&gt;
&lt;html lang="es"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;title&gt;Índice de Temas del Pagador&lt;/title&gt;
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            background: #fff;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #ecf0f1;
            margin: 5px 0;
            padding: 10px 15px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        li:hover {
            background: #d5dbdb;
        }
        a {
            text-decoration: none;
            color: #2980b9;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
        .badge {
            background-color: #e74c3c;
            color: white;
            padding: 2px 6px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }
    </style>
&lt;/head&gt;
&lt;body&gt;

&lt;div class="container"&gt;
    &lt;h1&gt;Índice de Temas del Pagador&lt;/h1&gt;
    &lt;p&gt;Bienvenido al panel de gestión de pagos. Seleccione un tema para ver los detalles.&lt;/p&gt;
    
    &lt;!-- Placeholder for dynamic content --&gt;
    &lt;ul id="payerTopicsList"&gt;
        &lt;!-- Items will be populated via JavaScript --&gt;
        &lt;li&gt;Cargando temas...&lt;/li&gt;
    &lt;/ul&gt;
&lt;/div&gt;

&lt;script&gt;
    // Simulated data for demonstration purposes
    const payerTopics = [
        { id: 1, title: "Configuración de Métodos de Pago", status: "Activo" },
        { id: 2, title: "Historial de Transacciones", status: "Histórico" },
        { id: 3, title: "Políticas de Reembolso", status: "Vigente" },
        { id: 4, title: "Gestión de Suscripciones", status: "Activo" },
        { id: 5, title: "Facturación y Facturas", status: "Archivado" }
    ];

    const listContainer = document.getElementById('payerTopicsList');

    // Clear loading message
    listContainer.innerHTML = '';

    // Populate the list
    payerTopics.forEach(topic => {
        const li = document.createElement('li');
        li.innerHTML = `
            &lt;a href="#topic-${topic.id}"&gt;${topic.title}&lt;/a&gt;
            &lt;span class="badge"&gt;${topic.status}&lt;/span&gt;
        `;
        listContainer.appendChild(li);
    });
&lt;/script&gt;

&lt;/body&gt;
&lt;/html&gt;

<style>
/* Ajustar diseño para índice de ancho completo */
.VPDoc {
  padding: 32px 48px 64px !important;
}
</style>

