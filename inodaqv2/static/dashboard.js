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

$(document).ready(function() {
  $('#btn-read-digital').click(function() {
    $.ajax({
      url: "",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        action: "dread",
      }),
      success: function(response) {
        console.log(response.rv);
        $("#digital-a0").text(response.A0);
        $("#digital-a1").text(response.A1);
        $("#digital-a2").text(response.A2);
        $("#digital-a3").text(response.A3);
        $("#digital-a4").text(response.A4);
        $("#digital-a5").text(response.A5);
      }
    });
  });
});

$(document).ready(function() {
  $('#pwm-sliders input[type="range"]').click(function() {
    $.ajax({
      url: "",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        action: "pwm",
        pin: $(this).attr("id"),
        value: $(this).val(),
      }),
      success: function(response) {
        console.log(response.rv);
      }
    });
  });
});
