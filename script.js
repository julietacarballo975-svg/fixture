// CUENTA REGRESIVA

const cuenta = document.getElementById('countdown');

const fechaMundial = new Date('Jun 11, 2026 00:00:00').getTime();

setInterval(() => {

    const ahora = new Date().getTime();

    const diferencia = fechaMundial - ahora;

    const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));

    cuenta.innerHTML = dias + ' dias para el Mundial';

}, 1000);

// BUSCADOR

const buscador = document.getElementById('buscar');

buscador.addEventListener('keyup', () => {

    const texto = buscador.value.toLowerCase();

    const cards = document.querySelectorAll('.card-partido');

    cards.forEach(card => {

        if(card.innerText.toLowerCase().includes(texto)){
            card.style.display = 'block';
        }
        else{
            card.style.display = 'none';
        }
    });
});