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
        if (response.rv) {
          $("#res-dig-" + response.pin).text(response.state);
        }
        else {
          $("#res-dig-" + response.pin).text("ERR");
          $("#row-alert-msg").text("Failed to set digital pin. Check terminal for error");
          $("#row-alert").fadeIn(250);
          $("#row-alert").delay(2000).fadeOut(250);
        }
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
        if (response.rv) {
          $("#res-pwm-" + response.pin).text(response.pwm);
        }
        else {
          $("#res-pwm-" + response.pin).text("ERR");
          $("#row-alert-msg").text("Failed to set PWM duty cycle. Check terminal for error");
          $("#row-alert").fadeIn(250);
          $("#row-alert").delay(2000).fadeOut(250);
        }
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
        if (response.rv) {
          $("#analog-a0").text(response.A0);
          $("#analog-a1").text(response.A1);
          $("#analog-a2").text(response.A2);
          $("#analog-a3").text(response.A3);
          $("#analog-a4").text(response.A4);
          $("#analog-a5").text(response.A5);
        }
        else {
          $("#row-alert-msg").text("Failed to read analog pins. Check terminal for error");
          $("#row-alert").fadeIn(250);
          $("#row-alert").delay(2000).fadeOut(250);
          $("#analog-a0").text("ERR");
          $("#analog-a1").text("ERR");
          $("#analog-a2").text("ERR");
          $("#analog-a3").text("ERR");
          $("#analog-a4").text("ERR");
          $("#analog-a5").text("ERR");
        }
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
        if (response.rv) {
          $("#digital-a0").text(response.A0);
          $("#digital-a1").text(response.A1);
          $("#digital-a2").text(response.A2);
          $("#digital-a3").text(response.A3);
          $("#digital-a4").text(response.A4);
          $("#digital-a5").text(response.A5);
        }
        else {
          $("#row-alert-msg").text("Failed to read digital pins. Check terminal for error");
          $("#row-alert").fadeIn(250);
          $("#row-alert").delay(2000).fadeOut(250);
          $("#digital-a0").text("ERR");
          $("#digital-a1").text("ERR");
          $("#digital-a2").text("ERR");
          $("#digital-a3").text("ERR");
          $("#digital-a4").text("ERR");
          $("#digital-a5").text("ERR");
        }
      }
    });
  });
});

$(document).ready(function() {
  $('#tone-radios input[type="radio"]').click(function() {
    $.ajax({
      url: "",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        action: "tone",
        pin: $(this).attr("id"),
        frequency: $("#tone-freq").val(),
      }),
      success: function(response) {
        if (!response.rv) {
          $("#row-alert-msg").text("Failed to set tone. Check terminal for error");
          $("#row-alert").fadeIn(250);
          $("#row-alert").delay(2000).fadeOut(250);
        }
      }
    });
  });
});
