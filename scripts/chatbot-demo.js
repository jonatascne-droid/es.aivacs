/* ===================================================
   AIVACS — chatbot-demo.js
   Demo interactiva de un chatbot de WhatsApp para una empresa de reformas,
   conectado (de forma simulada) a Obra Organize, Emite Fácil y a una agenda.
   Todos los datos son ficticios; en un proyecto real cada "consulta" es una
   llamada a la API del sistema del cliente (normalmente orquestada con n8n).
   =================================================== */
(function () {
  const chat = document.getElementById('wa-mensajes');
  const form = document.getElementById('wa-form');
  const input = document.getElementById('wa-input');
  const estado = document.getElementById('wa-estado');
  const chips = document.getElementById('wa-chips');
  const log = document.getElementById('bot-log');
  const reiniciar = document.getElementById('bot-reiniciar');
  if (!chat || !form || !input) return;

  /* ---------- Datos ficticios (los mismos clientes de la demo de Obra Organize / Emite Fácil) ---------- */
  const CLIENTES = [
    {
      nombre: 'Lucía Romero Gil', ref: 'P-2026-031', obra: 'Reparación de humedades',
      direccion: 'C/ Toledo 48, 3º B · Madrid', estado: 'pendiente',
      partidas: [['Tratamiento antihumedad (12 m²)', 190], ['Pintura antimoho', 95], ['Mano de obra', 65]],
      fase: 'Pendiente de aprobación', progreso: 0, factura: null,
    },
    {
      nombre: 'Javier Fernández Soto', ref: 'P-2026-027', obra: 'Reparación de tejado',
      direccion: 'Av. de la Paz 12 · Alcalá de Henares', estado: 'aprobado',
      partidas: [['Sustitución de tejas (35 m²)', 780], ['Impermeabilización', 520], ['Mano de obra', 200]],
      fase: 'Impermeabilización', progreso: 70, proximaVisita: 'lunes 29/09 a las 9:00',
      factura: { numero: 'A-10', fecha: '23/09/2026', pagada: true },
    },
    {
      nombre: 'Marta Iglesias Rey', ref: 'P-2026-029', obra: 'Cambio de ventanas',
      direccion: 'C/ Alcalá 210, 5º A · Madrid', estado: 'aprobado',
      partidas: [['6 ventanas PVC oscilobatientes', 1900], ['Retirada de ventanas antiguas', 250], ['Instalación', 350]],
      fase: 'Fabricación de las ventanas', progreso: 40, proximaVisita: 'jueves 02/10 a las 11:30',
      factura: { numero: 'A-12', fecha: '25/09/2026', pagada: false },
    },
    {
      nombre: 'Andrés Molina Prieto', ref: 'P-2026-022', obra: 'Reforma de baño completa',
      direccion: 'C/ Mayor 5 · Getafe', estado: 'aprobado',
      partidas: [['Demolición y retirada', 450], ['Fontanería y sanitarios', 1650], ['Alicatado y solado', 1300], ['Mano de obra', 566.94]],
      fase: 'Alicatado', progreso: 65, proximaVisita: 'miércoles 01/10 a las 8:30',
      factura: { numero: 'A-11', fecha: '24/09/2026', pagada: true },
    },
  ];
  const IVA = 0.21;
  const PRECIO_M2 = { 'Reforma de cocina': [450, 750], 'Reforma de baño': [550, 900], 'Pintura': [9, 15], 'Reforma integral': [650, 1100] };
  const HUECOS = ['martes 30/09 · 10:00', 'miércoles 01/10 · 16:30', 'viernes 03/10 · 9:00'];

  /* ---------- Utilidades ---------- */
  const esperar = (ms) => new Promise((r) => setTimeout(r, ms));
  const eur = (v) => v.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  const hora = () => new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
  const normalizar = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  function escapar(s) {
    return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  // Formato de WhatsApp: *negrita* y _cursiva_. El texto se escapa antes, así lo que escribe el usuario nunca se interpreta como HTML.
  function formatear(s) {
    return escapar(s)
      .replace(/\*([^*\n]+)\*/g, '<strong>$1</strong>')
      .replace(/(^|\s)_([^_\n]+)_/g, '$1<em>$2</em>')
      .replace(/\n/g, '<br>');
  }
  const totalPartidas = (c) => c.partidas.reduce((s, p) => s + p[1], 0);

  /* ---------- Render ---------- */
  function bajar() { chat.scrollTop = chat.scrollHeight; }

  function burbuja(lado, html, extraClase) {
    const div = document.createElement('div');
    div.className = 'wa-msg wa-' + lado + (extraClase ? ' ' + extraClase : '');
    const checks = lado === 'out'
      ? '<svg class="wa-check" viewBox="0 0 18 11" aria-hidden="true"><path d="M1 5.5l3.2 3.2L11 1.8M7 8.7l.5.5L17 1.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      : '';
    div.innerHTML = '<div class="wa-cuerpo">' + html + '</div><span class="wa-hora">' + hora() + checks + '</span>';
    chat.appendChild(div);
    bajar();
    return div;
  }

  function documento(nombre, detalle, texto) {
    const html =
      '<div class="wa-doc"><span class="wa-doc-icono">PDF</span><span class="wa-doc-info"><span class="wa-doc-nombre">' +
      escapar(nombre) + '</span><span class="wa-doc-detalle">' + escapar(detalle) + '</span></span></div>' +
      (texto ? '<div class="wa-doc-texto">' + formatear(texto) + '</div>' : '');
    burbuja('in', html, 'wa-msg-doc');
  }

  function registrar(sistema, texto, resultado) {
    if (!log) return;
    const vacio = log.querySelector('.bot-log-vacio');
    if (vacio) vacio.remove();
    const li = document.createElement('li');
    li.className = 'bot-log-item';
    li.innerHTML =
      '<span class="bot-log-sis bot-sis-' + sistema.clave + '">' + escapar(sistema.nombre) + '</span>' +
      '<span class="bot-log-texto">' + formatear(texto) + '</span>' +
      (resultado ? '<span class="bot-log-res">' + formatear(resultado) + '</span>' : '');
    log.appendChild(li);
    log.scrollTop = log.scrollHeight;
  }
  const SIS = {
    wa: { clave: 'wa', nombre: 'WhatsApp API' },
    n8n: { clave: 'n8n', nombre: 'n8n' },
    obra: { clave: 'obra', nombre: 'Obra Organize' },
    emite: { clave: 'emite', nombre: 'Emite Fácil' },
    agenda: { clave: 'agenda', nombre: 'Google Calendar' },
    crm: { clave: 'crm', nombre: 'CRM' },
  };

  let ocupado = false;
  async function responder(textos, pausa) {
    for (const t of [].concat(textos)) {
      estado.textContent = 'escribiendo…';
      await esperar(pausa || (typeof t === 'function' ? 900 : Math.min(1400, 500 + t.length * 6)));
      estado.textContent = 'en línea';
      if (typeof t === 'function') t(); else burbuja('in', formatear(t));
    }
  }

  function ponerChips(lista) {
    chips.innerHTML = '';
    lista.forEach((c) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'wa-chip';
      b.textContent = c;
      b.addEventListener('click', () => enviar(c));
      chips.appendChild(b);
    });
  }

  /* ---------- Conversación ---------- */
  const MENU =
    '¡Hola! 👋 Soy el asistente virtual de *Reformas Martín*.\nEscribe el número de lo que necesitas:\n\n' +
    '1️⃣ Consultar mi presupuesto\n2️⃣ Estado de mi obra\n3️⃣ Descargar mi factura\n4️⃣ Pedir un presupuesto nuevo\n' +
    '5️⃣ Agendar una visita técnica\n6️⃣ Hablar con una persona\n\nPara volver aquí, escribe *menú* o *0*.';
  const CHIPS_MENU = ['1', '2', '3', '4', '5', '6'];
  const CHIPS_NOMBRES = ['Lucía Romero', 'Javier Fernández', 'Andrés Molina', 'Marta Iglesias'];

  let estadoConv = 'menu';
  let cliente = null;
  let nuevo = {};

  async function mostrarMenu() {
    estadoConv = 'menu';
    cliente = null;
    await responder(MENU);
    ponerChips(CHIPS_MENU);
  }

  function buscarCliente(texto) {
    const partes = normalizar(texto).split(/\s+/).filter((p) => p.length >= 2);
    if (partes.length === 0) return [];
    return CLIENTES.filter((c) => {
      const nombre = normalizar(c.nombre).split(/\s+/);
      return partes.every((p) => nombre.some((n) => n.startsWith(p)));
    });
  }

  async function pedirNombre(siguiente, motivo) {
    estadoConv = siguiente;
    await responder('Claro. Para buscar ' + motivo + ', escríbeme tu *nombre completo* (o al menos nombre y apellido).');
    ponerChips(CHIPS_NOMBRES);
  }

  async function identificar(texto, sistema, consulta) {
    registrar(SIS.n8n, 'Mensaje recibido → flujo *' + consulta + '*');
    registrar(sistema, 'Buscando cliente “' + texto.trim() + '”…');
    estado.textContent = 'escribiendo…';
    await esperar(900);
    const encontrados = buscarCliente(texto);
    if (encontrados.length === 1) {
      registrar(sistema, 'Cliente encontrado', '*' + encontrados[0].nombre + '* · ' + encontrados[0].ref);
      return encontrados[0];
    }
    registrar(sistema, encontrados.length ? 'Varios resultados' : 'Sin resultados', encontrados.length + ' coincidencias');
    if (encontrados.length > 1) {
      await responder('Encontré ' + encontrados.length + ' clientes con ese nombre: ' + encontrados.map((c) => '*' + c.nombre + '*').join(', ') + '. ¿Me escribes el nombre completo?');
    } else {
      await responder('No encontré ningún cliente con ese nombre 🤔\nRevisa cómo lo escribiste o prueba con uno de la demo: _Lucía Romero_, _Javier Fernández_, _Andrés Molina_ o _Marta Iglesias_.\n\nEscribe *0* para volver al menú.');
    }
    ponerChips(CHIPS_NOMBRES.concat(['0']));
    return null;
  }

  async function mostrarPresupuesto(c) {
    const base = totalPartidas(c);
    const total = Math.round(base * (1 + IVA) * 100) / 100;
    const lineas = c.partidas.map((p) => '• ' + p[0] + ': ' + eur(p[1])).join('\n');
    registrar(SIS.obra, 'Generando PDF del presupuesto *' + c.ref + '*', 'OK');
    await responder('¡Te encontré, *' + c.nombre.split(' ')[0] + '*! Aquí tienes tu presupuesto 👇');
    await esperar(500);
    documento(
      'Presupuesto_' + c.ref + '.pdf', 'PDF · 2 páginas · 96 kB',
      '*' + c.obra + '*\n📍 ' + c.direccion + '\n\n' + lineas + '\n\nBase: ' + eur(base) + '\nIVA (21 %): ' + eur(total - base) +
      '\n*Total: ' + eur(total) + '*\n\nEstado: ' + (c.estado === 'pendiente' ? '🟡 Pendiente de aprobación' : '🟢 Aprobado')
    );
    if (c.estado === 'pendiente') {
      estadoConv = 'orc_accion';
      cliente = c;
      await responder('¿Qué quieres hacer?\n\n1️⃣ Aprobar el presupuesto\n2️⃣ Tengo dudas, quiero hablar con el técnico\n0️⃣ Volver al menú');
      ponerChips(['1', '2', '0']);
    } else {
      estadoConv = 'fin';
      await responder('Este presupuesto ya está aprobado ✅. ¿Te ayudo con algo más? Escribe *0* para ver el menú.');
      ponerChips(['0']);
    }
  }

  async function aprobarPresupuesto(c) {
    const total = Math.round(totalPartidas(c) * (1 + IVA) * 100) / 100;
    registrar(SIS.obra, 'Presupuesto *' + c.ref + '* → estado “aprobado”', 'OK');
    registrar(SIS.emite, 'Creando pedido y factura Verifactu', 'Factura *A-13* · ' + eur(total));
    registrar(SIS.agenda, 'Creando tarea “Planificar inicio de obra”', 'OK');
    await responder([
      '¡Genial! ✅ Presupuesto *' + c.ref + '* aprobado.\n\nYa avisamos al equipo de obra y generamos tu factura.',
      () => documento('Factura_A-13.pdf', 'PDF · 1 página · 64 kB', '*Factura A-13* · Verifactu ✔️\nImporte: *' + eur(total) + '*\n\n💳 Puedes pagarla con tarjeta desde el enlace seguro que te enviamos por email.'),
      'Un técnico te escribirá en menos de 24 h para fijar la fecha de inicio. ¿Algo más? Escribe *0* para el menú.',
    ]);
    c.estado = 'aprobado';
    estadoConv = 'fin';
    ponerChips(['0']);
  }

  async function mostrarObra(c) {
    if (c.progreso === 0) {
      await responder('Tu obra *' + c.obra + '* todavía no ha empezado: el presupuesto está pendiente de aprobación. Escribe *1* en el menú para verlo y aprobarlo.');
    } else {
      const llenos = Math.round(c.progreso / 10);
      const barra = '▓'.repeat(llenos) + '░'.repeat(10 - llenos);
      registrar(SIS.obra, 'Consultando avance de *' + c.obra + '*', c.progreso + ' %');
      registrar(SIS.agenda, 'Próxima visita del equipo', c.proximaVisita);
      await responder('🏗️ *' + c.obra + '*\n📍 ' + c.direccion + '\n\nFase actual: *' + c.fase + '*\n' + barra + ' ' + c.progreso + ' %\n\n📅 Próxima visita del equipo: *' + c.proximaVisita + '*\n\nTe avisaremos por aquí cuando cambie de fase.');
    }
    estadoConv = 'fin';
    await responder('¿Te ayudo con algo más? Escribe *0* para ver el menú.');
    ponerChips(['0']);
  }

  async function mostrarFactura(c) {
    if (!c.factura) {
      registrar(SIS.emite, 'Buscando facturas de *' + c.nombre + '*', '0 facturas');
      await responder('Todavía no tienes facturas emitidas: se genera cuando apruebas el presupuesto. ¿Quieres verlo? Escribe *1* después de volver al menú (*0*).');
    } else {
      const total = Math.round(totalPartidas(c) * (1 + IVA) * 100) / 100;
      registrar(SIS.emite, 'Buscando facturas de *' + c.nombre + '*', 'Factura *' + c.factura.numero + '*');
      await responder([
        'Aquí tienes tu factura 🧾',
        () => documento('Factura_' + c.factura.numero + '.pdf', 'PDF · 1 página · 61 kB',
          '*Factura ' + c.factura.numero + '* · ' + c.factura.fecha + '\n' + c.obra + '\nImporte: *' + eur(total) + '*\nVerifactu: registrada en la AEAT ✔️\nEstado: ' + (c.factura.pagada ? '🟢 Pagada' : '🟡 Pendiente de pago')),
      ]);
      if (!c.factura.pagada) await responder('Puedes pagarla con tarjeta en el enlace seguro que te enviamos por email 💳');
    }
    estadoConv = 'fin';
    await responder('¿Algo más? Escribe *0* para ver el menú.');
    ponerChips(['0']);
  }

  async function humano() {
    estadoConv = 'humano';
    registrar(SIS.crm, 'Conversación asignada a una persona del equipo', 'Notificación enviada');
    await responder('Ok, un momento. En cuanto sea posible, *Martín* te responde por aquí.\n\n✅ Estás en *atención humana*.\nSi quieres volver al menú, escribe *0*.');
    ponerChips(['0']);
  }

  async function procesar(texto) {
    const t = normalizar(texto);
    registrar(SIS.wa, 'Mensaje del cliente: “' + texto.trim().slice(0, 60) + '”');

    if (['0', 'menu', 'hola', 'buenas', 'inicio'].includes(t)) return mostrarMenu();

    switch (estadoConv) {
      case 'menu':
      case 'fin':
        if (t === '1') return pedirNombre('orc_nombre', 'tu presupuesto en nuestro sistema');
        if (t === '2') return pedirNombre('obra_nombre', 'tu obra');
        if (t === '3') return pedirNombre('fact_nombre', 'tus facturas');
        if (t === '4') {
          estadoConv = 'nuevo_tipo';
          nuevo = {};
          await responder('¡Perfecto! Te hago 3 preguntas rápidas para una estimación.\n\n¿Qué tipo de obra necesitas?\n1️⃣ Reforma de cocina\n2️⃣ Reforma de baño\n3️⃣ Pintura\n4️⃣ Reforma integral');
          return ponerChips(['1', '2', '3', '4']);
        }
        if (t === '5') {
          estadoConv = 'visita';
          registrar(SIS.agenda, 'Consultando huecos libres del técnico', HUECOS.length + ' huecos');
          await responder('Estos son los próximos huecos libres del técnico 📅\n\n' + HUECOS.map((h, i) => (i + 1) + '️⃣ ' + h).join('\n') + '\n\nEscribe el número del que prefieras.');
          return ponerChips(['1', '2', '3', '0']);
        }
        if (t === '6') return humano();
        await responder('No entendí 😅. Escribe el *número* de una opción o *0* para ver el menú.');
        return ponerChips(CHIPS_MENU);

      case 'orc_nombre': {
        const c = await identificar(texto, SIS.obra, 'consultar presupuesto');
        if (c) return mostrarPresupuesto(c);
        return;
      }
      case 'orc_accion':
        if (t === '1') return aprobarPresupuesto(cliente);
        if (t === '2') return humano();
        await responder('Escribe *1* para aprobar, *2* para hablar con el técnico o *0* para el menú.');
        return ponerChips(['1', '2', '0']);

      case 'obra_nombre': {
        const c = await identificar(texto, SIS.obra, 'estado de la obra');
        if (c) return mostrarObra(c);
        return;
      }
      case 'fact_nombre': {
        const c = await identificar(texto, SIS.emite, 'descargar factura');
        if (c) return mostrarFactura(c);
        return;
      }

      case 'nuevo_tipo': {
        const tipos = Object.keys(PRECIO_M2);
        const i = parseInt(t, 10) - 1;
        if (!(i >= 0 && i < tipos.length)) {
          await responder('Escribe un número del *1* al *4*.');
          return ponerChips(['1', '2', '3', '4']);
        }
        nuevo.tipo = tipos[i];
        estadoConv = 'nuevo_m2';
        await responder('*' + nuevo.tipo + '* 👍\n¿Cuántos *metros cuadrados* aproximados tiene la zona? (solo el número)');
        return ponerChips(['8', '15', '60']);
      }
      case 'nuevo_m2': {
        const m2 = parseFloat(t.replace(',', '.'));
        if (!(m2 > 0 && m2 < 2000)) {
          await responder('Escríbeme solo el número de m², por ejemplo *12*.');
          return ponerChips(['8', '15', '60']);
        }
        nuevo.m2 = m2;
        estadoConv = 'nuevo_nombre';
        await responder('Por último, ¿a nombre de quién hago la solicitud?');
        return ponerChips(['Carmen López']);
      }
      case 'nuevo_nombre': {
        nuevo.nombre = texto.trim().slice(0, 60);
        const [min, max] = PRECIO_M2[nuevo.tipo];
        registrar(SIS.crm, 'Nuevo lead: *' + nuevo.nombre + '* · ' + nuevo.tipo, 'Guardado');
        registrar(SIS.obra, 'Creando solicitud de presupuesto', 'Solicitud *S-0042*');
        await responder([
          'Gracias, *' + nuevo.nombre + '* 🙌\n\nEstimación orientativa para *' + nuevo.tipo + '* de ' + nuevo.m2 + ' m²:\n*' + eur(min * nuevo.m2) + ' – ' + eur(max * nuevo.m2) + '* (IVA no incluido)',
          'Creé tu solicitud *S-0042*. Un técnico te llamará en menos de 24 h para concretar el presupuesto final.\n\n¿Quieres agendar ya la visita técnica? Escribe *5* (o *0* para el menú).',
        ]);
        estadoConv = 'fin';
        return ponerChips(['5', '0']);
      }

      case 'visita': {
        const i = parseInt(t, 10) - 1;
        if (!(i >= 0 && i < HUECOS.length)) {
          await responder('Escribe *1*, *2* o *3* para elegir el hueco.');
          return ponerChips(['1', '2', '3', '0']);
        }
        registrar(SIS.agenda, 'Reservando visita: ' + HUECOS[i], 'Evento creado');
        registrar(SIS.wa, 'Programado recordatorio 24 h antes', 'OK');
        await responder('📅 ¡Visita confirmada para el *' + HUECOS[i] + '*!\nTe enviaremos un recordatorio por aquí 24 h antes.\n\n¿Algo más? Escribe *0* para el menú.');
        estadoConv = 'fin';
        return ponerChips(['0']);
      }

      case 'humano':
        // En atención humana el bot no responde: el mensaje queda para la persona del equipo.
        registrar(SIS.crm, 'Mensaje reenviado al equipo', 'Pendiente de respuesta');
        return;
    }
  }

  async function enviar(texto) {
    const limpio = String(texto || '').trim();
    if (!limpio || ocupado) return;
    ocupado = true;
    chips.innerHTML = '';
    burbuja('out', formatear(limpio.slice(0, 300)));
    try { await procesar(limpio.slice(0, 300)); } finally { ocupado = false; }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const v = input.value;
    input.value = '';
    enviar(v);
  });

  async function iniciar() {
    chat.innerHTML = '<div class="wa-fecha">HOY</div><div class="wa-aviso">🔒 Demo interactiva de AIVACS con datos ficticios. Escribe o toca las respuestas rápidas.</div>';
    if (log) log.innerHTML = '<li class="bot-log-vacio">Envía un mensaje y verás aquí cada consulta a los otros sistemas, en tiempo real.</li>';
    estadoConv = 'menu';
    ocupado = true;
    await mostrarMenu();
    ocupado = false;
  }

  if (reiniciar) reiniciar.addEventListener('click', () => { if (!ocupado) iniciar(); });

  // Empieza cuando el teléfono aparece en pantalla, para que se vea al bot "escribiendo".
  const telefono = document.getElementById('wa-telefono');
  if ('IntersectionObserver' in window && telefono) {
    const obs = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { obs.disconnect(); iniciar(); }
    }, { threshold: 0.25 });
    obs.observe(telefono);
  } else {
    iniciar();
  }
})();
