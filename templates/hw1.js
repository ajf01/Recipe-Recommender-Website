function showDialog() {
  var dialog = document.querySelector('dialog');
  console.log('Fired');
  dialog.show();
  setTimeout(function () {
      dialog.close();
    }, 3000);
}