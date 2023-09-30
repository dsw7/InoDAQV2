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
        console.log(response.rv);
      }
    });
  });
});

$(document).ready(function() {
  $('#btn-read-analog').click(function() {
    $.ajax({
      url: "",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        action: "aread",
      }),
      success: function(response) {
        console.log(response.rv);
        $("#analog-a0").text(response.A0);
        $("#analog-a1").text(response.A1);
        $("#analog-a2").text(response.A2);
        $("#analog-a3").text(response.A3);
        $("#analog-a4").text(response.A4);
        $("#analog-a5").text(response.A5);
      }
    });
  });
});
