timeout_id = undefined;
empty = true;
num_back = 2;
time_empty = 2500;
time_full = 500;
window.number_history = [0, 0, 0, 0];
start_time = undefined;
correct = 0;
failures = 0;
chances = 0;
run_time = 120;
pressed = false;
chance_to_succeed = 25;
already_guessed = true;

function end_game() {
    var infoSpan = $('#infoSpan');
    infoSpan.text('Konec.');
    infoSpan.removeClass();
    infoSpan.addClass('orange');
    console.log('chances: ' + chances);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/nback/' + num_back + '/save', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        chances: chances,
        failures: failures,
        correct: correct,
    }));
}

function get_timestamp() {
    return Math.floor(Date.now() / 1000);
}

function make_full(n) {
  console.log('number ' + n + ' active');
  window.number_history.push(n);
  empty = false;
  already_guessed = false;
  toggle(n);
  timeout_id = setTimeout(function(){ make_empty(n); }, time_full);
}

function make_empty(n) {
    console.log(document.activeElement);
  console.log('clearing board');
    var infoSpan = $('#infoSpan');
    infoSpan.text('');
    infoSpan.removeClass();
  if (check_success()) {
    chances += 1;
    console.log('chance');
  }
  var now = get_timestamp();
  console.log('time',  now - start_time);
  if (now - start_time > run_time) {
      end_game();
      return;
  }
  empty = true;
  toggle(n);
  next = gen_number(n);
  timeout_id = setTimeout(function(){ make_full(next); }, time_empty);
}

function toggle(n) {
  var row = Math.ceil(n / 3);
  var col = n - (row - 1) * 3;
  $('table tr:nth-child('+row+') td:nth-child('+col+')').toggleClass('fill');
}

function clear_board() {
  $('td').removeClass('fill');
}

function check_success() {
  var last = window.number_history[window.number_history.length - 1];
  var to_check = window.number_history[window.number_history.length - 1 - num_back];
  if (last == 0 || to_check == 0) {
    return false;
  }
  if (last == to_check) {
    return true;
  }
}

function gen_number(last) {
    var matching_number = window.number_history[window.number_history.length - num_back];
    if (matching_number != 0) {
        var repeat = Math.floor(Math.random() * 100) + 1;
        if (repeat < chance_to_succeed) {
            return matching_number;
        }
    }
    var n = Math.floor(Math.random() * 9) + 1;
    while (n == last) {
        n = Math.floor(Math.random() * 9) + 1;
    }
    return n;
}

function start_game() {
    if (!pressed) {
        return;
    }
    console.log('starting game');
    correct = 0;
    failures = 0;
    misses = 0;
    window.number_history = [0, 0, 0, 0]
    start_time = get_timestamp();
    var n = gen_number(0);
    make_full(n);
}

function space_pressed() {
  if (!already_guessed) {
      already_guessed = true;
    if (check_success()) {
      correct += 1;
      console.log('correct');
      var infoSpan = $('#infoSpan');
      infoSpan.text('Pravilno!');
      infoSpan.removeClass();
      infoSpan.addClass('green');
    } else {
      failures += 1;
      console.log('failure');
      var infoSpan = $('#infoSpan');
      infoSpan.text('Napaka!');
      infoSpan.removeClass();
      infoSpan.addClass('red');
    }
  }
}


function press_to_start(n) {
    console.log('starting with ', n);
    num_back = n;
    pressed = true;
    setTimeout(function(){ start_game(); }, time_empty);
}
