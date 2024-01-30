async function changePrefix() {
    var value = document.getElementById('prefix').value;
    if (Number.isInteger(parseInt(value)) == true) {
      fetch('/changePrefix/' + value, {
        method: 'POST',
      }).then(response => {
        document.getElementById('prefix').value = '';
        document.location.reload();
      });
    }
  }

  document.getElementById("changePrefix").addEventListener("click", (event )=>{
    changePrefix();
  }); 

document.getElementById("dwl").addEventListener("click", (event )=>{
  if (!window.confirm('Esto puede demorar un poco'))
  event.preventDefault();
}); 

document.getElementById("dlt").addEventListener("click", (event )=>{
  if (!window.confirm('Esto eliminara todo el contenido de la prueba. ¿Continuar?'))
  event.preventDefault();
});

