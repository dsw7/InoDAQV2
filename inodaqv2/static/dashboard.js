$(document).ready(function() {
  $('#digital-pins input[type="checkbox"]').click(function() {
    $.ajax({
      url: "",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        action: "dig",
        pin: $(this).attr("id"),
        state: $(this).is(":checked"),
      }),
      success: function(response) {
        console.log("The command was: " + response.command);
        console.log("The reply was: " + response.message);
      }
    });
  });
});
