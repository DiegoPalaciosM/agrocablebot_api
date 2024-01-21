async function changePrefix() {
    var value = document.getElementById('prefix').value;
    if (Number.isInteger(parseInt(value)) == true) {
      fetch('/changePrefix/' + value, {
        method: 'GET',
      }).then(response => {
        document.getElementById('prefix').value = '';
        document.location.reload();
      });
    }
  }
