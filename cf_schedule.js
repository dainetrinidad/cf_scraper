$(document).ready(function() {
  $(".slot").append('<div class="attendance"></div>');
  for (var item in wishlists) {
    console.log(item);
    for (var i = 0; i < wishlists[item].length; i++) {
      console.log(wishlists[item][i]);
      session_id = wishlists[item][i];
      $("#session_" + session_id + " .attendance").append(
        '<span class="person ' + item + '">' + item.toUpperCase() + "</span>"
      );
    }
  }
});
