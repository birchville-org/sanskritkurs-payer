---
aside: false
outline: false
---

# Índice de Gramática

El Índice Gramatical enumera todos los temas y fenómenos gramáticos del curso de sánscrito y permite un acceso rápido a lecciones específicas.

\<!DOCTYPE html\>
\<html lang="es"\>
\<head\>
    \<meta charset="UTF-8"\>
    \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>
    \<title\>Índice de Temas del Pagador\</title\>
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
\</head\>
\<body\>

\<div class="container"\>
    \<h1\>Índice de Temas del Pagador\</h1\>
    \<p\>Bienvenido al panel de gestión de pagos. Seleccione un tema para ver los detalles.\</p\>
    
    \<!-- Placeholder for dynamic content -→
    \<ul id="payerTopicsList"\>
        \<!-- Items will be populated via JavaScript -→
        \<li\>Cargando temas...\</li\>
    \</ul\>
\</div\>

\<script\>
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
            \<a href="#topic-${topic.id}"\>${topic.title}\</a\>
            \<span class="badge"\>${topic.status}\</span\>
        `;
        listContainer.appendChild(li);
    });
\</script\>

\</body\>
\</html\>

<style>
/* Ajustar diseño para índice de ancho completo */
.VPDoc {
  padding: 32px 48px 64px !important;
}
</style>

