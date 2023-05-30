document.addEventListener('DOMContentLoaded', function () {
    const consultaForm = document.getElementById('consulta-form');
    const registroForm = document.getElementById('registro-form');
    const saldoForm = document.getElementById('saldo-form');
    const resultDiv = document.getElementById('result');

    consultaForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value;
        const apellidos = document.getElementById('apellidos').value;

        fetch(`http://192.168.119.140:6901/saldo?nombre=${nombre}&apellidos=${apellidos}`)
            .then(response => response.json())
            .then(data => {
                resultDiv.innerHTML = `Saldo: ${data.saldo}`;
            })
            .catch(error => {
                resultDiv.innerHTML = 'Error en la consulta.';
            });
    });

    registroForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('reg-nombre').value;
        const apellidos = document.getElementById('reg-apellidos').value;

        fetch('http://192.168.119.140:6901/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                apellidos: apellidos
            })
        })
            .then(response => response.json())
            .then(data => {
                resultDiv.innerHTML = data.mensaje;
            })
            .catch(error => {
                resultDiv.innerHTML = 'Error en el registro.';
            });
    });

    saldoForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('saldo-nombre').value;
        const apellidos = document.getElementById('saldo-apellidos').value;
        const ingreso = parseFloat(document.getElementById('saldo-ingreso').value);

        fetch('http://192.168.119.140:6901/ingreso', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                apellidos: apellidos,
                ingreso: ingreso
            })
        })
            .then(response => response.json())
            .then(data => {
                resultDiv.innerHTML = data.mensaje;
            })
            .catch(error => {
                resultDiv.innerHTML = 'Error al agregar saldo.';
            });
    });
});
